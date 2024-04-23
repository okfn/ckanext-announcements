import datetime
import logging
from pytz import timezone
from ckan import model
from ckan.plugins import toolkit
from ckanext.announcements.models import Announcement


log = logging.getLogger(__name__)


def get_public_announcements():
    """Get a list of Announcements"""
    # display messages up to 3 days after they disappeared.
    now = datetime.datetime.now()
    messages = (
        model.Session.query(Announcement)
        .filter_by(status="active")
        .filter(Announcement.to_date > now, Announcement.from_date < now)
        .limit(10)
        .all()
    )
    messages = _apply_tz(messages)
    return messages


def get_all_announcements():
    """Get a list of Announcements"""
    # TODO this should be paginated
    limit = toolkit.config.get("ckanext.announcements.limit_announcements", 50)
    messages = (
        model.Session.query(Announcement)
        .order_by(Announcement.timestamp.desc())
        .limit(limit)
        .all()
    )
    messages = _apply_tz(messages)
    return messages


def _apply_tz(messages):
    """Apply the timezone to the messages"""
    display_timezone = toolkit.config.get("ckan.display_timezone")
    tz = timezone(display_timezone)
    for message in messages:
        message.from_date = message.from_date.astimezone(tz)
        message.to_date = message.to_date.astimezone(tz)
    return messages
