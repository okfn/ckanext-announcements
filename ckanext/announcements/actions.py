from ckan import model
from ckan.plugins import toolkit
from ckanext.announcements.models import Announcement


def announcement_create(context, data_dict):
    toolkit.check_access('announcement_create', context, data_dict)
    m = context.get('model', model)
    
    announcement = Announcement(
        timestamp=data_dict['timestamp'],
        user_creator_id=data_dict['user_creator_id'],
        from_date=data_dict['from_date'],
        to_date=data_dict['to_date'],
        message=data_dict['message'],
        status=data_dict['status'],
    )
    m.Session.add(announcement)
    m.Session.commit()
    m.Session.refresh(announcement)
    
    return announcement.dictize()


@toolkit.side_effect_free
def announcement_show(context, data_dict):
    m = context.get('model', model)
    toolkit.check_access('announcement_show', context, data_dict)

    announcement = m.Session.query(Announcement).get(data_dict['id'])
    if announcement:
        return announcement.dictize()

    raise toolkit.ObjectNotFound("Announcement not found")
