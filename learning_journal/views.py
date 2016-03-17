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

dict_list = [entry1, entry2, entry3]

# templates/base.jinja2
@view_config(route_name='home', renderer='templates/list.jinja2')
def list_view(request):
    return 


@view_config(route_name='entry', renderer='string')
def detail_view(request):
    return 'You selected entry number: {entry}'.format(**request.matchdict)
