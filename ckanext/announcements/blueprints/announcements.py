from flask import Blueprint
import ckan.plugins.toolkit as toolkit
from ckanext.unhcr.utils import require_user

announcements_blueprint = Blueprint(
    'announcements',
    __name__,
    url_prefix=u'/ckan-admin/announcements'
)


@require_user
def index():
    try:
        toolkit.check_access('sysadmin', {'user': toolkit.c.user})
    except toolkit.NotAuthorized:
        return toolkit.abort(403, 'Not authorized to manage Announcements')

    return toolkit.render('admin/announcements.html')


announcements_blueprint.add_url_rule(
    rule=u'/',
    view_func=index,
    methods=['GET',],
    strict_slashes=False,
)
