import datetime
import factory
from ckan import model
from ckantoolkit.tests import helpers
from ckanext.announcements.models import Announcement


class Announcement(factory.Factory):
    class Meta:
        model = Announcement

    _user = helpers.call_action("get_site_user")
    user_creator_id = _user['name']
    from_date = datetime.datetime.utcnow() + datetime.timedelta(days=3)
    to_date = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    message = 'This is an announcement message'
    status = 'active'

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        gm = target_class(**kwargs)
        model.Session.add(gm)
        model.Session.commit()
        model.Session.remove()
        return gm
