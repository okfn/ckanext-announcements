from types import SimpleNamespace
import pytest
from ckan.plugins import toolkit
from ckanext.announcements import auth
from ckanext.announcements.tests import factories
from ckanext.announcements.blueprints import get_dates


@pytest.fixture
def an_data():
    """test setup data"""
    obj = SimpleNamespace()
    # Create CKAN users
    obj.regular_user = factories.UserMulti()
    obj.sysadmin = factories.SysadminUserMulti()

    return obj


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestAnnouncementsUI:
    def test_regular_user(self, app, an_data):
        environ = {"Authorization": an_data.regular_user["token"]}

        resp = app.get("/ckan-admin/announcements", headers=environ)
        assert resp.status_code == 403

    def test_sysadmin_user(self, app, an_data):
        environ = {"Authorization": an_data.sysadmin["token"]}

        resp = app.get("/ckan-admin/announcements", headers=environ)
        assert resp.status_code == 200
        assert 'name="_csrf_token"' in resp.text

    def test_invalid_timezone_is_validation_error(self):
        with pytest.raises(toolkit.ValidationError) as error:
            get_dates(
                {
                    "from_date": "2026-09-15T10:00",
                    "to_date": "2026-09-15T11:00",
                    "timezone": "Not/A_Timezone",
                }
            )

        assert "date" in error.value.error_dict

    def test_anonymous_user_is_not_authorized(self):
        result = auth.announcement_create({"auth_user_obj": None}, {})

        assert result == {"success": False}
