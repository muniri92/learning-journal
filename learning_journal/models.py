
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Unicode,
)

import datetime
import markdown
from wtforms import (
    Form,
    StringField,
    TextAreaField,
    # validators,
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
    """Create New Entry in Entries Table."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(120))
    text = Column(Unicode)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def markdown_text(self):
        md = markdown.Markdown(safe_mode='replace', html_replacement_text='--RAW HTML NOT ALLOWED--')
        return md.convert(self.text)

class NewEntry(Form):
    """Create Form for New Entry."""

    title = StringField('Title')
    text = TextAreaField('Text')
