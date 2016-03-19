from pyramid import testing
from learning_journal.models import Entry
from learning_journal.models import DBSession


def test_empty_listing(app):
    response = app.get('/')
    assert response.status_code == 200
    actual = response.body
    expected = b"No entries here so far"
    assert expected in actual


def test_view_entry(app, new_entry):
    new_entry_id = new_entry.id
    response = app.get('/entry/{}'.format(new_entry_id))
    assert response.status_code == 200


def test_edit_entry(app, new_entry):
    new_entry_id = new_entry.id
    response = app.get('/{}/edit'.format(new_entry_id))
    assert response.status_code == 200


def test_edit(app, new_entry):
    title = new_entry.title
    text = new_entry.text
    entry_dict = {'title': title, 'text': text}
    app.post('/{}/edit'.format(new_entry.id), params=entry_dict, status='3*')
    results = DBSession.query(Entry).filter(
        Entry.title == title and Entry.text == text)
    assert results.count() == 1


def test_add_entry(app, new_entry):
    response = app.get('/write')
    assert response.status_code == 200


def test_add(app):
    results = DBSession.query(Entry).filter(
        Entry.title == 'title' and Entry.text == 'text')
    assert results.count() == 0
    entry_dict = {'title': 'title', 'text': 'text'}
    app.post('/write', params=entry_dict, status='3*')
    results = DBSession.query(Entry).filter(
        Entry.title == 'title' and Entry.text == 'text')
    assert results.count() == 1


def test_view(dbtransaction, new_entry):
    from .. views import list_view
    from .. views import detail_view
    test_request = testing.DummyRequest()
    list_dict = list_view(test_request)

    entry = list_dict['entries'][0]
    test_request.matchdict = {'entry': entry.id}
    entry_dict = detail_view(test_request)
    assert entry_dict['entry'] == entry == new_entry
