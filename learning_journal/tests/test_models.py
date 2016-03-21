from learning_journal.models import Entry
from learning_journal.models import DBSession


def test_create_entry(dbtransaction):
    new_entry = Entry(title="Test Title", text="ipsum")
    assert new_entry.id is None
    DBSession.add(new_entry)
    DBSession.flush()
    assert new_entry.id is not None
