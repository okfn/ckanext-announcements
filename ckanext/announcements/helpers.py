import datetime
import logging
from ckan import model
from ckan.plugins import toolkit
from ckanext.announcements.models import Announcement


log = logging.getLogger(__name__)


def get_announcements(limit=50):
    """ Get a list of Announcements """
    # TODO this should be paginated
    limit = toolkit.config.get('ckanext.announcements.limit_announcements', limit)
    # display messages up to 3 days after they disappeared.
    until = datetime.datetime.utcnow() - datetime.timedelta(days=3)
    messages = model.Session.query(
        Announcement
    ).filter_by(
        status="active"
    ).filter(
        Announcement.to_date > until
    ).order_by(
        Announcement.timestamp.desc()
    ).limit(limit).all()

    return messages
