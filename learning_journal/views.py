from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from wtforms import Form, BooleanField, StringField, validators

import pyramid.httpexceptions as ex

import transaction
from .models import (
    DBSession,
    Entry,
    NewEntry,
    )


@view_config(route_name='home', renderer='templates/list.jinja2')
def list_view(request):
    entries = DBSession.query(Entry).all()
    return {'entries': entries}


@view_config(route_name='add_entry', renderer='templates/add.jinja2')
def add_new(request):
    # entry = Entry()
    form = NewEntry(request.POST)
    title = form.title.data
    text = form.text.data

    if request.POST and form.validate():
        entry = Entry(title=title, text=text)
        # form.populate._obj(entry)
        # entry.save()
        DBSession.add(entry)
        DBSession.flush()
        transaction.commit()
        this_entry = DBSession.query(Entry).filter(Entry.title == title).first()
        # new_id = this_entry.id
        raise ex.HTTPFound(request.route_url('/entry/{}'.format(this_entry.id)))
    # raise ex.HTTPFound(request.route_url('/write'))
    return {'form': form}


@view_config(route_name='entry', renderer='templates/entry.jinja2')
def detail_view(request):
    this_id = '{entry}'.format(**request.matchdict)
    this_entry = DBSession.query(Entry).filter(Entry.id == this_id).first()
    return {'entry': this_entry}

