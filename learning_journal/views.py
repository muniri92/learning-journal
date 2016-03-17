from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Entry,
    )


entry1 = {
    'id': '7',
    'title': 'ALL CATS',
    'created': '3/14/16',
}
entry2 = {
    'id': '2',
    'title': 'ALL DOGS',
    'created': '3/14/16',
}

entry3 = {
    'id': '1',
    'title': 'ALL STARFISH',
    'created': '3/14/16',
}

dict_list = [entry1, entry2, entry3]

# templates/base.jinja2
@view_config(route_name='home', renderer='templates/list.jinja2')
def list_view(request):
    entries = DBSession.query(Entry).all()
    return {'dict': entries}


@view_config(route_name='entry', renderer='string')
def detail_view(request):
    return 'You selected entry number: {entry}'.format(**request.matchdict)
