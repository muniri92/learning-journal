# -*- coding: utf-8 -*-
"""Conftest."""
import os
import pytest
from sqlalchemy import create_engine
from learning_journal.models import DBSession, Base, Entry
from passlib.hash import sha256_crypt

user = os.environ.get('USER', 'MunirIbrahim')
TEST_DATABASE_URL = 'postgresql://{}:password@localhost:5432/test_learning'.format(user)
AUTH_DATA = {'username': 'muniri', 'password': 'muniri'}

# FIXTURES FOR AUTHORIZATION
# *******************************************


@pytest.fixture()
def authenticated_app(app, auth_env):
    """Create an auth app we can us to test."""
    app.post('/login', AUTH_DATA)
    return app


@pytest.fixture()
def auth_env():
    """Create was auth password in env we can use."""
    os.environ['AUTH_USERNAME'] = 'muniri'
    os.environ['AUTH_PASSWORD'] = sha256_crypt.encrypt('muniri')


# MAIN FIXTURES
# *******************************************


@pytest.fixture(scope='session')
def sqlengine(request):
    """I don't really know what this does."""
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    """Implement a new dbtransaction for testing."""
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection, expire_on_commit=False)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture()
def app(dbtransaction):
    """Implement a new session."""
    from learning_journal import main
    from webtest import TestApp
    fakesettings = {"sqlalchemy.url": TEST_DATABASE_URL}
    app = main({}, **fakesettings)
    return TestApp(app)


@pytest.fixture(scope='function')
def new_entry(request, auth_env):
    """Create a fake entry."""
    add_entry = Entry(title='heyheyhey', text='1111')
    DBSession.add(add_entry)
    DBSession.flush()

    def teardown():
        DBSession.query(Entry).filter(Entry.id == add_entry.id).delete()
        DBSession.flush()

    request.addfinalizer(teardown)
    return add_entry
