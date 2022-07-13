"""
Announcement auth functions
"""

def announcement_create(context, data_dict):
    """ Only sysadmins are allowed """
    user_obj = context.get('auth_user_obj')
    return {'success': user_obj.sysadmin}


def announcement_show(context, data_dict):
    return {'success': True}
