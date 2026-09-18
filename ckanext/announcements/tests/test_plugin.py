from datetime import datetime, timedelta
from types import SimpleNamespace
import pytest
from ckan import model
from ckan.plugins import toolkit

from ckanext.announcements.helpers import (
    get_all_announcements,
    get_public_announcements,
    dictize_announ,
)
from ckanext.announcements.models import Announcement
from ckanext.announcements.tests import factories
from ckanext.announcements.validators import validate_announcement


@pytest.fixture
def an_data():
    """test setup data"""
    obj = SimpleNamespace()
    obj.old_announcement = factories.Announcement(
        message="This is an old message",
        from_date=datetime.now() - timedelta(days=7),
        to_date=datetime.now() - timedelta(days=6),
    )
    obj.active_announcement = factories.Announcement(
        message="This should be a public message",
        from_date=datetime.now() - timedelta(days=1),
        to_date=datetime.now() + timedelta(days=1),
    )
    return obj


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestAnnouncements:
    def test_announcement_saved(self, an_data):
        """Test single announcement saved correctly"""
        assert an_data.old_announcement.message == "This is an old message"
        assert an_data.old_announcement.status == "active"

    def test_get_all_announcements_helper(self, an_data):
        """Test all messages helper"""
        ga = get_all_announcements()
        assert len(ga) == 2

    def test_get_public_announcements_helper(self, an_data):
        """Test public messages helper"""
        ga = get_public_announcements()
        assert len(ga) == 1
        assert ga[0]['message'] == "This should be a public message"

    def test_rendering_does_not_mutate_model_dates(self, an_data):
        announcement = model.Session.get(
            Announcement, an_data.active_announcement.id
        )
        original_from_date = announcement.from_date
        original_to_date = announcement.to_date

        dictize_announ([announcement])

        assert announcement.from_date == original_from_date
        assert announcement.to_date == original_to_date

    def test_end_date_must_be_after_start_date(self):
        start = datetime.now()
        with pytest.raises(toolkit.ValidationError) as error:
            validate_announcement(
                {
                    "from_date": start,
                    "to_date": start - timedelta(minutes=1),
                    "message": "Invalid range",
                }
            )

        assert "to_date" in error.value.error_dict
