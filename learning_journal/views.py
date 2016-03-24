"""View for the blog."""
from pyramid.view import view_config, forbidden_view_config
# from wtforms import Form, BooleanField, StringField, validators
import pyramid.httpexceptions as ex

from .models import (
    DBSession,
    Entry,
    NewEntry,
)
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from .security import check_password


@view_config(route_name='home', renderer='templates/list.jinja2',
             permission='view',)
def list_view(request):
    """Show list of entry."""
    entries = DBSession.query(Entry).order_by(Entry.created.desc()).all()
    return {'entries': entries}


@view_config(route_name='entry', renderer='templates/entry.jinja2',
             permission='view')
def detail_view(request):
    """Show current entry."""
    this_id = request.matchdict['entry']
    this_entry = DBSession.query(Entry).get(this_id)
    if this_entry is None:
        raise ex.HTTPNotFound()
    return {'entry': this_entry}


@view_config(route_name='add_entry', renderer='templates/add.jinja2',
             permission='edit')
def add_new(request):
    """Add new entry."""
    form = NewEntry(request.POST)
    if request.POST and form.validate():
        entry = Entry(title=form.title.data, text=form.text.data)
        DBSession.add(entry)
        DBSession.flush()
        return ex.HTTPFound(request.route_url('entry', entry=entry.id))
    return {'form': form}


@view_config(route_name="edit_entry", renderer="templates/edit.jinja2",
             permission='edit')
def edit_existing(request):
    """Edit exisiting entry."""
    post_id = request.matchdict['entry']
    this_entry = DBSession.query(Entry).filter(Entry.id == post_id).first()
    form = NewEntry(request.POST, this_entry)

    if request.POST and form.validate():
        form.populate_obj(this_entry)
        return ex.HTTPFound(request.route_url('entry', entry=post_id))
    return {'form': form}


@view_config(route_name="login", renderer="templates/login.jinja2",
             permission='view')
@forbidden_view_config(renderer="templates/login.jinja2")
def login(request):
    """Login in to edit and/or add entry."""
    username = request.params.get('username', '')
    password = request.params.get('password', '')
    if request.method == 'POST':
        if check_password(password):
            headers = remember(request, username)
            return HTTPFound(request.route_url('home'), headers=headers)
    return {}


@view_config(route_name='logout', permission='edit')
def logout(request):
    """Logout."""
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
