from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Entry,
    )


# templates/base.jinja2
@view_config(route_name='home', renderer='string')
def list_view(request):
    return 'This is the list view'


@view_config(route_name='entry', renderer='string')
def detail_view(request):
    return 'You selected entry number: {entry}'.format(**request.matchdict)
