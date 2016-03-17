from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Entry,
    )

@view_config(route_name='home', renderer='templates/list.jinja2')
def list_view(request):
    entries = DBSession.query(Entry).all()
    return {'entries': entries}


@view_config(route_name='entry', renderer='templates/entry.jinja2')
def detail_view(request):
    this_id = '{entry}'.format(**request.matchdict)
    this_entry = DBSession.query(Entry).filter(Entry.id == this_id).first()
    return {'entry': this_entry}
