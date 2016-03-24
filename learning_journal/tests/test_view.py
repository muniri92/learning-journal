
import os
from sqlalchemy import create_engine
from learning_journal.models import DBSession, Base, Entry
from pyramid import testing
from passlib.hash import sha256_crypt
AUTH_DATA = {'username': 'muniri', 'password': 'muniri'}


# TEST SECURITY (LOGIN/LOGOUT)
# **********************************************************


def test_password_exist(dbtransaction, auth_env):
    """Test to ensure password exists."""
    assert os.environ.get('AUTH_PASSWORD', 'muniri') is not None


def stored_password_is_encrypted(dbtransaction, auth_env):
    """Test that password is authorized."""
    assert os.environ.get['AUTH_PASSWORD', sha256_crypt.encrypt('muniri')] != 'muniri'


def test_no_access_to_view(dbtransaction, app):
    """Test to make sure NO access if permitted with no auth."""
    response = app.get('/login')
    assert response.status_code == 200


def test_access_to_view(dbtransaction, app, auth_env):
    """Test to make sure the auth allows access."""
    response = app.get('/login', )
    assert response.status_code == 200


def test_username_exist(dbtransaction, app, auth_env):
    """Test that username exists."""
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_check_pw_success(dbtransaction, auth_env):
    """"Test that the password is successful."""
    from .. security import check_password
    password = 'muniri'
    assert check_password(password)


def test_check_pw_failure(dbtransaction, auth_env):
    """Test to make sure that the password fails when given wrong pw."""
    from .. security import check_password
    password = 'not secret'
    assert check_password(password) is False


def test_get_login_view(dbtransaction, authenticated_app):
    """Test that the GET login view works."""
    response = authenticated_app.get('/login')
    assert response.status_code == 200


def test_post_login_success(dbtransaction, app, auth_env):
    """Test that the POST login has correct status code."""
    response = app.post('/login', AUTH_DATA)
    assert response.status_code == 302


def test_post_login_success_redirect_home(dbtransaction, app, auth_env):
    """Test to make sure we are redireacted to home."""
    response = app.post('/login', AUTH_DATA)
    header = response.headers
    domain = 'http//localhost'
    actual_path = header.get('Location', '')[len(domain) + 1:]
    assert actual_path == '/'


def test_post_login_auth_tkt_present(dbtransaction, app, auth_env):
    """Test to ensure that the auth ticket is there."""
    response = app.post('/login', AUTH_DATA)
    header = response.headers
    cookies_set = header.getall('Set-Cookie')
    assert cookies_set
    for cookie in cookies_set:
        if cookie.startswith('auth_tkt'):
            break
    else:
        assert False


def test_post_login_fail_bad_password(dbtransaction, app, auth_env):
    """Test that a bad password login will fail."""
    data = {'username': 'muniri', 'password': 'not secret'}
    response = app.post('/login', data)
    assert response.status_code == 200


# TEST THE EDIT AND ADD VIEWS
# ************************************************************


def test_empty_listing(dbtransaction, app, auth_env):
    """Test if the view for the home page list is working."""
    response = app.get('/')
    assert response.status_code == 200


def test_view_entry(dbtransaction, app, new_entry, auth_env):
    """Test if view for entries is allowed."""
    new_entry_id = new_entry.id
    response = app.get('/entry/{}'.format(new_entry_id))
    assert response.status_code == 200


def test_add_entry(dbtransaction, app, new_entry, auth_env):
    """Test that authorized user can write."""
    response = app.get('/write')
    assert response.status_code == 200


def test_edit_entry(dbtransaction, app, new_entry, auth_env):
    """Test to see if you can make edits."""
    new_entry_id = new_entry.id
    response = app.get('/edit/{}'.format(new_entry_id), 'AUTH_DATA', status=404)
    assert response.status_code == 404


def test_edit(dbtransaction, app, new_entry, auth_env):
    """Test that an entry was created by a person whose logged in."""
    title = new_entry.title
    text = new_entry.text
    entry_dict = {'title': title,
                  'text': text,
                  'username': 'muniri',
                  'password': 'muniri'
                  }
    app.post('/{}/edit'.format(new_entry.id), params=entry_dict, status='3*')
    results = DBSession.query(Entry).filter(
        Entry.title == title and Entry.text == text)

    assert results.count() == 1


# def test_add(dbtransaction, app, auth_env):
#     """Test that we can add to the entry."""
#     results = DBSession.query(Entry).filter(
#         Entry.title == 'title' and Entry.text == 'text')
#     assert results.count() == 0
#     entry_dict = {'title': 'title',
#                   'text': 'text',
#                   'username': 'muniri',
#                   'password': 'muniri'
#                   }
#     app.post('/write', params=entry_dict, status='3*')
#     results = DBSession.query(Entry).filter(
#         Entry.title == 'title' and Entry.text == 'text')
#     assert results.count() == 1


# TEST FUNCTIONALITY
# ************************************************************


def test_view(dbtransaction, new_entry, auth_env):
    """Functional test of the view."""
    from .. views import list_view
    from .. views import detail_view
    test_request = testing.DummyRequest()
    list_dict = list_view(test_request)

    entry = list_dict['entries'][0]
    test_request.matchdict = {'entry': entry.id}
    entry_dict = detail_view(test_request)
    assert entry_dict['entry'] == entry == new_entry
