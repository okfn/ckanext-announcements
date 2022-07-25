from datetime import datetime, timedelta
import pytest

from ckanext.announcements.helpers import (
    get_all_announcements,
    get_public_announcements,
)
from ckanext.announcements.tests import factories


@pytest.mark.usefixtures("clean_db", "announcement_migrate")
class TestAnnouncements:
    def setup(self):
        self.old_announcement = factories.Announcement(
            message="This is an old message",
            from_date=datetime.now() - timedelta(days=7),
            to_date=datetime.now() - timedelta(days=6),
        )
        self.active_announcement = factories.Announcement(
            message="This should be a public message",
            from_date=datetime.now() - timedelta(days=1),
            to_date=datetime.now() + timedelta(days=1),
        )

    def test_announcement_saved(self):
        """Test single announcement saved correctly"""
        assert self.old_announcement.message == "This is an old message"
        assert self.old_announcement.status == "active"

    def test_get_all_announcements_helper(self):
        """Test all messages helper"""
        ga = get_all_announcements()
        assert len(ga) == 2

    def test_get_public_announcements_helper(self):
        """Test public messages helper"""
        ga = get_public_announcements()
        assert len(ga) == 1
        assert ga[0].message == "This should be a public message"
