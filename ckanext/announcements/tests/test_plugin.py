from datetime import datetime, timedelta
import pytest

from ckanext.announcements.helpers import (
    get_all_announcements,
    get_public_announcements,
)
from ckanext.announcements.tests import factories


@pytest.mark.usefixtures("clean_db", "announcement_migrate")
class TestAnnouncements:
    def test_announcement_saved(self):
        old_announcement = factories.Announcement(
            message="This is an old message",
            from_date=datetime.now() - timedelta(days=7),
            to_date=datetime.now() - timedelta(days=6),
        )

        """ Test single announcement saved correctly """
        assert old_announcement.message == "This is an old message"
        assert old_announcement.status == "active"

    def test_get_all_announcements_helper(self):

        factories.Announcement(
            message="This is an old message",
            from_date=datetime.now() - timedelta(days=7),
            to_date=datetime.now() - timedelta(days=6),
        )
        factories.Announcement(
            message="This should be a public message",
            from_date=datetime.now() - timedelta(days=1),
            to_date=datetime.now() + timedelta(days=1),
        )

        """ Test all messages helper """
        ga = get_all_announcements()
        assert len(ga) == 2

    def test_get_public_announcements_helper(self):

        factories.Announcement(
            message="This is an old message",
            from_date=datetime.now() - timedelta(days=7),
            to_date=datetime.now() - timedelta(days=6),
        )
        factories.Announcement(
            message="This should be a public message",
            from_date=datetime.now() - timedelta(days=1),
            to_date=datetime.now() + timedelta(days=1),
        )

        """ Test public messages helper """
        ga = get_public_announcements()
        assert len(ga) == 1
        assert ga[0].message == "This should be a public message"
