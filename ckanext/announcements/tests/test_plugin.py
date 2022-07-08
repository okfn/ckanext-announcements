import pytest

from ckanext.announcements.helpers import get_announcements
from ckanext.announcements.tests import factories


@pytest.mark.usefixtures('clean_db', 'announcement_migrate')
class TestAnnouncements:

    def setup(self):
        self.announcement = factories.Announcement(
            message='This is an announcement message'
        )

    def test_announcement_saved(self):
        """ Test single announcement saved correctly """
        assert self.announcement.message == 'This is an announcement message'
        assert self.announcement.status == 'active'

    def test_get_announcements_helper(self):
        """ Test helper """
        ga = get_announcements()
        assert len(ga) == 1

