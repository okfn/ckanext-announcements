import datetime
import factory
from ckan import model
from ckantoolkit import check_ckan_version
from ckantoolkit.tests import factories, helpers
from ckanext.announcements.models import Announcement


class UserMulti(factories.User):
    """Multi version of a CKAN user"""

    @factory.post_generation
    def token(obj, create, extracted, **kwargs):
        if not create:
            return
        if check_ckan_version(min_version="2.10"):
            api_token = factories.APIToken(
                user=obj["id"],
                expires_in=30,
                unit=4,
            )
            obj["token"] = api_token["token"]
        else:
            obj["token"] = obj["apikey"]


class SysadminUserMulti(UserMulti):
    sysadmin = True


class Announcement(factory.Factory):
    class Meta:
        model = Announcement

    _user = helpers.call_action("get_site_user")
    user_creator_id = _user["name"]
    from_date = datetime.datetime.utcnow() + datetime.timedelta(days=3)
    to_date = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    message = "This is an announcement message"
    status = "active"

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        gm = target_class(**kwargs)
        model.Session.add(gm)
        model.Session.commit()
        model.Session.remove()
        return gm
