from pyramid.view import view_config
from wtforms import Form, BooleanField, StringField, validators
import pyramid.httpexceptions as ex
import markdown
from jinja2 import Markup
from .models import (
    DBSession,
    Entry,
    NewEntry,
)


@view_config(route_name='home', renderer='templates/list.jinja2')
def list_view(request):
    entries = DBSession.query(Entry).order_by(Entry.created.desc()).all()
    return {'entries': entries}


@view_config(route_name='entry', renderer='templates/entry.jinja2')
def detail_view(request):
    this_id = request.matchdict['entry']
    this_entry = DBSession.query(Entry).get(this_id)
    if this_entry is None:
        raise ex.HTTPNotFound()
    this_entry.text = Markup(markdown.markdown(this_entry.text))
    return {'entry': this_entry}


@view_config(route_name='add_entry', renderer='templates/add.jinja2')
def add_new(request):
    form = NewEntry(request.POST)
    if request.POST and form.validate():
        entry = Entry(title=form.title.data, text=form.text.data)
        DBSession.add(entry)
        DBSession.flush()
        return ex.HTTPFound(request.route_url('entry', entry=entry.id))
    return {'form': form}


@view_config(route_name="edit_entry", renderer="templates/edit.jinja2")
def edit_existing(request):
    post_id = request.matchdict['entry']
    this_entry = DBSession.query(Entry).filter(Entry.id == post_id).first()
    form = NewEntry(request.POST, this_entry)

    if request.POST and form.validate():
        form.populate_obj(this_entry)
        return ex.HTTPFound(request.route_url('entry', entry=post_id))
    return {'form': form}
