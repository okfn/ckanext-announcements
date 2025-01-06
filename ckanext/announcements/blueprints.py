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
    # apply the selected tuimezone
    from_date = datetime.strptime(from_date, "%Y-%m-%dT%H:%M")
    from_date = pytz.timezone(timezone).localize(from_date)
    to_date = datetime.strptime(to_date, "%Y-%m-%dT%H:%M")
    to_date = pytz.timezone(timezone).localize(to_date)
    return from_date, to_date


def create():
    """Create (POST) a new announcement"""

    user_obj = toolkit.c.userobj
    user_creator_id = user_obj.id
    from_date, to_date = get_dates(toolkit.request.form)
    message = toolkit.request.form.get("message")

    new_announcements_data = {
        "timestamp": datetime.now(),
        "user_creator_id": user_creator_id,
        "from_date": from_date,
        "to_date": to_date,
        "message": message,
        "status": "active",
    }
    try:
        toolkit.get_action("announcement_create")(
            {"user": user_obj.name}, new_announcements_data
        )
    except toolkit.ValidationError as e:
        summary = ", ".join([v[0] for k, v in e.error_dict.items()])
        message = "Error creating new announcement: {}.".format(summary)
        toolkit.h.flash_error(message)

    return toolkit.redirect_to("announcements.index")


def update():
    """Updates an announcement"""

    user_obj = toolkit.c.userobj
    announ_id = toolkit.request.form.get("id")
    from_date, to_date = get_dates(toolkit.request.form)

    message = toolkit.request.form.get("message")

    announcements_data = {
        "id": announ_id,
        "from_date": from_date,
        "to_date": to_date,
        "message": message,
    }
    try:
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
