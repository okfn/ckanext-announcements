from types import SimpleNamespace
import pytest
from ckanext.announcements.tests import factories, helpers


@pytest.fixture
def an_data():
    """test setup data"""
    obj = SimpleNamespace()
    # Create CKAN 2.9/2.10 users
    obj.regular_user = factories.UserMulti()
    obj.sysadmin = factories.SysadminUserMulti()

    return obj


@pytest.mark.usefixtures("clean_db", "announcement_migrate", "with_request_context")
class TestAnnouncementsUI:
    def test_regular_user(self, app, an_data):
        environ = helpers.get_user_env(an_data.regular_user)

        resp = app.get("/ckan-admin/announcements", headers=environ)
        assert resp.status_code == 403

    def test_sysadmin_user(self, app, an_data):
        environ = helpers.get_user_env(an_data.sysadmin)

        resp = app.get("/ckan-admin/announcements", headers=environ)
        assert resp.status_code == 200
