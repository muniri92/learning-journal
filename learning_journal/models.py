from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Unicode,
)
import datetime

from wtforms import Form, StringField, TextAreaField, validators

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    """Create New Entry in Entries Table."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(120))
    text = Column(Unicode)
    created = Column(DateTime, default=datetime.datetime.utcnow)


class NewEntry(Form):
    """Create Form for New Entry."""

    title = StringField('Title')
    text = TextAreaField('Text')
