import datetime
import logging
from ckan import model
from ckan.plugins import toolkit
from ckanext.announcements.models import Announcement


log = logging.getLogger(__name__)


def get_public_announcements():
    """ Get a list of Announcements """
    # display messages up to 3 days after they disappeared.
    now = datetime.datetime.utcnow()
    messages = model.Session.query(
        Announcement
    ).filter_by(
        status="active"
    ).filter(
        Announcement.to_date > now,
        Announcement.from_date < now
    ).limit(10).all()

    return messages


def get_all_announcements():
    """ Get a list of Announcements """
    # TODO this should be paginated
    limit = toolkit.config.get('ckanext.announcements.limit_announcements', 50)
    messages = model.Session.query(
        Announcement
    ).order_by(
        Announcement.timestamp.desc()
    ).limit(limit).all()

    return messages
