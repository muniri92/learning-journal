# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine
from learning_journal.models import DBSession, Base, Entry
import os


user = os.environ.get('USER', 'MunirIbrahim')
TEST_DATABASE_URL = 'postgresql://{}:password@localhost:5432/test_learning'.format(user)


@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
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
    from learning_journal import main
    from webtest import TestApp
    fakesettings = {"sqlalchemy.url": TEST_DATABASE_URL}
    app = main({}, **fakesettings)
    return TestApp(app)


@pytest.fixture(scope='function')
def new_entry(request):
    """Create a fake entry."""
    add_entry = Entry(title='heyheyhey', text='1111')
    DBSession.add(add_entry)
    DBSession.flush()

    def teardown():
        DBSession.query(Entry).filter(Entry.id == add_entry.id).delete()
        DBSession.flush()

    request.addfinalizer(teardown)
    return add_entry


def test_no_access_to_view(app):
    response = app.get('/secure')
    assert response.status_code == 403
