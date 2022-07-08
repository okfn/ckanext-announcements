from flask import Blueprint
from ckan import logic, model
from ckan.common import g
from ckan.lib import base
from ckan.plugins import toolkit


announcements_blueprint = Blueprint(
    'announcements',
    __name__,
    url_prefix=u'/ckan-admin/announcements'
)


@announcements_blueprint.before_request
def before_request():
    try:
        context = dict(model=model, user=g.user, auth_user_obj=g.userobj)
        logic.check_access('sysadmin', context)
    except logic.NotAuthorized:
        base.abort(403, ('Need to be system administrator to administer'))


def index():
    return toolkit.render('admin/announcements.html')


announcements_blueprint.add_url_rule(
    rule=u'/',
    view_func=index,
    methods=['GET',],
    strict_slashes=False,
)
