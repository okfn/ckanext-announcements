import pytest

from ckan.plugins import toolkit


@pytest.fixture
def clean_db(reset_db, migrate_db_for):
    reset_db()
    if toolkit.check_ckan_version(min_version='2.11'):
        migrate_db_for("announcements")
    else:
        migrate_old()


def migrate_old():
    import contextlib
    from ckan.cli.db import _resolve_alembic_config
    import ckan.model as model

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

    _apply_alembic_migrations()
