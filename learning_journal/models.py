import datetime
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    timestamp,
    Datetime,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Text(120), convert_unicode=True)
    text = Column(Text, convert_unicode=True)
    created = Column(Datetime, default=datetime.datetime.utcnow)

Index('entry', Entry.title, unique=True, mysql_length=255)
