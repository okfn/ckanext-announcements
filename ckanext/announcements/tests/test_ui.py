from types import SimpleNamespace
import pytest
from ckanext.announcements.tests import factories


@pytest.fixture
def an_data():
    """test setup data"""
    obj = SimpleNamespace()
    # Create CKAN users
    obj.regular_user = factories.UserMulti()
    obj.sysadmin = factories.SysadminUserMulti()

    return obj


@pytest.mark.usefixtures("with_plugins", "clean_db", "announcement_migrate", "with_request_context")
class TestAnnouncementsUI:
    def test_regular_user(self, app, an_data):
        environ = {"Authorization": an_data.regular_user["token"]}

        resp = app.get("/ckan-admin/announcements", headers=environ)
        assert resp.status_code == 403

    def test_sysadmin_user(self, app, an_data):
        environ = {"Authorization": an_data.sysadmin["token"]}

        resp = app.get("/ckan-admin/announcements", headers=environ)
        assert resp.status_code == 200, f'Expected 200, got {resp.status_code}\n\t{environ}\n\t{resp.body}\n\t{an_data.sysadmin}'
