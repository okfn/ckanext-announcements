from ckanext.announcements.tests import factories


class TestAnnouncements:

    def setup(self):
        self.announcement = factories.Announcement(
            message='This is an announcement message'
        )

    def test_announcement_saved(self):
        assert self.announcement.message == 'This is an announcement message'
        assert self.announcement.status == 'active'
