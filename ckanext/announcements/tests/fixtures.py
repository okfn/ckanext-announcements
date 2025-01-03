import contextlib
import pytest

from ckan.plugins import toolkit
from ckan.cli.db import _resolve_alembic_config
import ckan.model as model


if toolkit.check_ckan_version(max_version='2.10'):

    # TODO: in the next CKAN release
    # there will be a more elegant way to achieve this
    @contextlib.contextmanager
    def _repo_for_plugin(plugin):
        original = model.repo._alembic_ini
        model.repo._alembic_ini = _resolve_alembic_config(plugin)
        try:
            yield model.repo
        finally:
            model.repo._alembic_ini = original

    def _apply_alembic_migrations():
        with _repo_for_plugin("announcements") as repo:
            repo.upgrade_db("head")

    @pytest.fixture
    def announcement_migrate():

        _apply_alembic_migrations()

else:

    @pytest.fixture
    def announcement_migrate(migrate_db_for):
        migrate_db_for('announcements')
