
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import (
    DBSession,
    Base,
)

from pyramid.authentication import AuthTktAuthenticationPolicy
from .security import DefaultRoot
import os
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.config import Configurator

from pyramid.view import view_config
from passlib.hash import sha256_crypt


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    database_url = os.environ.get('DATABASE_URL', None)
    if database_url is not None:
        settings['sqlalchemy.url'] = database_url
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    settings['auth.username'] = os.environ.get('AUTH_USERNAME', 'admin')
    settings['auth.password'] = os.environ.get(
        'AUTH_PASSWORD', sha256_crypt.encrypt('secret')
    )
    auth_secret = os.environ.get('JOURNAL_AUTH_SECRET', 'devmcfly')
    auth_tkt = AuthTktAuthenticationPolicy(
        secret=auth_secret,
    )
    auth_policy = ACLAuthorizationPolicy()
    config = Configurator(
        settings=settings,
        authentication_policy=auth_tkt,
        authorization_policy=auth_policy,
        root_factory=DefaultRoot
    )

    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('entry', '/entry/{entry}')
    config.add_route('add_entry', '/write')
    config.add_route('edit_entry', '/{entry}/edit')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
