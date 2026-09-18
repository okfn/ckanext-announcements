from datetime import datetime
import logging
import pytz
from flask import Blueprint
from ckan.plugins import toolkit
from ckanext.announcements.utils import require_sysadmin_user


log = logging.getLogger(__name__)
announcements_blueprint = Blueprint(
    "announcements", __name__, url_prefix="/ckan-admin/announcements"
)


@require_sysadmin_user
def index():
    """Get the Announcements home page"""
    display_timezone = toolkit.config.get("ckan.display_timezone", "UTC")
    pytz_timezones = pytz.all_timezones.copy()
    # remove CET and UTC to display them first
    pytz_timezones.remove("CET")
    pytz_timezones.remove("UTC")
    ctx = {
        "display_timezone": display_timezone,
        "timezones": ["UTC", "CET"] + sorted(pytz_timezones),
    }
    return toolkit.render("admin/announcements.html", extra_vars=ctx)


def get_dates(form):
    from_date = form.get("from_date")
    to_date = form.get("to_date")
    timezone = form.get("timezone")
    try:
        selected_timezone = pytz.timezone(timezone)
        from_date = selected_timezone.localize(
            datetime.strptime(from_date, "%Y-%m-%dT%H:%M"), is_dst=None
        )
        to_date = selected_timezone.localize(
            datetime.strptime(to_date, "%Y-%m-%dT%H:%M"), is_dst=None
        )
    except (TypeError, ValueError, pytz.exceptions.Error):
        raise toolkit.ValidationError(
            {"date": ["Dates and timezone must contain valid values"]}
        )
    return from_date, to_date


def create():
    """Create (POST) a new announcement"""

    user_obj = toolkit.c.userobj
    user_creator_id = user_obj.id
    try:
        from_date, to_date = get_dates(toolkit.request.form)
        new_announcements_data = {
            "timestamp": datetime.utcnow(),
            "user_creator_id": user_creator_id,
            "from_date": from_date,
            "to_date": to_date,
            "message": toolkit.request.form.get("message"),
            "status": "active",
        }
        toolkit.get_action("announcement_create")(
            {"user": user_obj.name}, new_announcements_data
        )
    except toolkit.ValidationError as e:
        summary = ", ".join(v[0] for v in e.error_dict.values())
        message = "Error creating new announcement: {}.".format(summary)
        toolkit.h.flash_error(message)

    return toolkit.redirect_to("announcements.index")


def update():
    """Updates an announcement"""

    user_obj = toolkit.c.userobj
    announ_id = toolkit.request.form.get("id")
    try:
        from_date, to_date = get_dates(toolkit.request.form)
        announcements_data = {
            "id": announ_id,
            "from_date": from_date,
            "to_date": to_date,
            "message": toolkit.request.form.get("message"),
        }
        toolkit.get_action("announcement_update")(
            {"user": user_obj.name}, announcements_data
        )
    except toolkit.ValidationError as e:
        summary = ", ".join([v[0] for _, v in e.error_dict.items()])
        message = "Error updating announcement: {}.".format(summary)
        toolkit.h.flash_error(message)

    return toolkit.redirect_to("announcements.index")


def delete():
    """Delete an announcement"""

    user_obj = toolkit.c.userobj
    announ_id = toolkit.request.form.get("id")

    try:
        toolkit.get_action("announcement_delete")(
            {"user": user_obj.name}, {"id": announ_id}
        )
    except toolkit.ValidationError as e:
        message = "Error deleting announcement: {}.".format(e)
        toolkit.h.flash_error(message)

    return toolkit.redirect_to("announcements.index")


announcements_blueprint.add_url_rule(rule="/", view_func=index, methods=["GET"], strict_slashes=False)
announcements_blueprint.add_url_rule(rule="/new", view_func=create, methods=["POST"], strict_slashes=False)
announcements_blueprint.add_url_rule(rule="/update", view_func=update, methods=["POST"], strict_slashes=False)
announcements_blueprint.add_url_rule(rule="/delete", view_func=delete, methods=["POST"], strict_slashes=False)
