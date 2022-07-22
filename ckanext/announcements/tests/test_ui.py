import pytest
from ckantoolkit.tests import factories as core_factories


@pytest.mark.usefixtures('clean_db', 'announcement_migrate', 'with_request_context')
class TestAnnouncementsUI:
    def setup(self):
        self.regular_user = core_factories.User(name='regular')
        self.sysadmin = core_factories.Sysadmin(name='sysadmin')

    def test_regular_user(self, app):
        environ = {
            'REMOTE_USER': self.regular_user['name']
        }

        resp = app.get('/ckan-admin/announcements', extra_environ=environ)
        assert resp.status_code == 403

    def test_sysadmin_user(self, app):
        environ = {
            'REMOTE_USER': self.sysadmin['name']
        }

        resp = app.get('/ckan-admin/announcements', extra_environ=environ)
        assert resp.status_code == 200
