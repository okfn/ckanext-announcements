from datetime import datetime
from flask import Blueprint
from ckan.lib import base
from ckan.plugins import toolkit


announcements_blueprint = Blueprint(
    'announcements',
    __name__,
    url_prefix=u'/ckan-admin/announcements'
)


def index():
    """ Get the Announcements home page """
    if not toolkit.c.userobj.sysadmin:
        base.abort(403, ('Need to be system administrator to administer'))
    return toolkit.render('admin/announcements.html')


def create():
    """ Create (POST) a new announcement """
    
    user_obj = toolkit.c.userobj
    user_creator_id = user_obj.id
    from_date = toolkit.request.form.get('from_date')
    to_date = toolkit.request.form.get('to_date')
    message = toolkit.request.form.get('message')

    new_announcements_data = {
        'timestamp': datetime.now(),
        'user_creator_id':user_creator_id,
        'from_date': datetime.fromisoformat(from_date),
        'to_date': datetime.fromisoformat(to_date),
        'message': message,
        'status': 'active',
    }
    try:
        toolkit.get_action('announcement_create')(
            {'user': user_obj.name},
            new_announcements_data
        )
    except toolkit.ValidationError as e:
        message = 'Error creating new announcement: {}.'.format(e)
        toolkit.h.flash_error(message)

    return toolkit.redirect_to('announcements.index')


def update():
    """ Updates an announcement """
    
    user_obj = toolkit.c.userobj
    announ_id = toolkit.request.form.get('id')
    from_date = toolkit.request.form.get('from_date')
    to_date = toolkit.request.form.get('to_date')
    message = toolkit.request.form.get('message')

    announcements_data = {
        'id': announ_id,
        'from_date': datetime.fromisoformat(from_date),
        'to_date': datetime.fromisoformat(to_date),
        'message': message,
    }
    try:
        toolkit.get_action('announcement_update')(
            {'user': user_obj.name},
            announcements_data
        )
    except toolkit.ValidationError as e:
        message = 'Error updating announcement: {}.'.format(e)
        toolkit.h.flash_error(message)

    return toolkit.redirect_to('announcements.index')


def delete():
    """ Delete an announcement """
    
    user_obj = toolkit.c.userobj
    announ_id = toolkit.request.form.get('id')

    try:
        toolkit.get_action('announcement_delete')(
            {'user': user_obj.name},
            {'id': announ_id}
        )
    except toolkit.ValidationError as e:
        message = 'Error deleting announcement: {}.'.format(e)
        toolkit.h.flash_error(message)

    return toolkit.redirect_to('announcements.index')


announcements_blueprint.add_url_rule(
    rule=u'/',
    view_func=index,
    methods=['GET',],
    strict_slashes=False,
)

announcements_blueprint.add_url_rule(
    rule=u'/new',
    view_func=create,
    methods=['POST',],
    strict_slashes=False,
)

announcements_blueprint.add_url_rule(
    rule=u'/update',
    view_func=update,
    methods=['POST',],
    strict_slashes=False,
)

announcements_blueprint.add_url_rule(
    rule=u'/delete',
    view_func=delete,
    methods=['POST',],
    strict_slashes=False,
)
