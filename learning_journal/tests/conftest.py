# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine

from learning_journal.models import DBSession, Base
import os


user = os.environ.get('USER', 'seleniumk')
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
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return connection

