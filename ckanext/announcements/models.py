import datetime
import logging

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.types import Enum, UnicodeText

from ckan.model.meta import metadata
from ckan.model.types import make_uuid


log = logging.getLogger(__name__)
Base = declarative_base(metadata=metadata)


class Announcement(Base):
    __tablename__ = u'announcements'

    id = Column(UnicodeText, primary_key=True, default=make_uuid)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_creator_id = Column(UnicodeText, nullable=False)

    from_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    to_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    message = Column(UnicodeText, nullable=True)

    status = Column(
        Enum('draft', 'active', 'deleted', name='announcements_status_enum'),
        default='draft',
        nullable=False,
    )
    extras = Column(MutableDict.as_mutable(JSONB), nullable=True)

    def dictize(self):
        dct = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        return dct
