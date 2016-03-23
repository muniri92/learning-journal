# import os
# import pytest
# import webtest
# import main


# # *************************************************


# # in views.py*
# # @view_config(route_name='secure', renderer='string', permission='templates/edit.jinja')
# # def secure(request):
# #     return


# # ***************************************************

# # <form action='', method='POST'>
# #     <div>Username:<input type='text'></div>
# #     <div>Password:<input type='password'></div>
# #     <div></div>
# # </form>


# # ***************************************************

# # in views.py*
# # view for login (create a ```config.add_route('login, /login')``` in __init__)
# from .security import check_pw
# # import HTTPForbidden


# @view_config(route_name='login', renderer='template/login.jinja2')
# def login(request):
#     if request.method == 'POST':
#         username = request.params.get('username', '')
#         password = request.params.get('password', '')
#         if check_pw(password):
#             headers = remember(request, username)
#             return HTTPFound(location='/', header=header)
#     return {}


# # ***************************************************

# # in the security.py*
# import os

# from passlib.apps import custom_app_context as pwd_context


# def check_pw(pw):
#     hashed = os.environ.get('AUTH_PASSWORD', 'this is not a password')
#     return pwd_context.verify(pw, hashed)


# # ***************************************************

# AUTH_DATA = {'username': 'admin', 'password': 'secret'}


# @pytest.fixture()
# def app():
#     """Create an app we can use."""
#     settings = {'sqlalchemy.url'}
#     app = main({}, **settings)
#     return webtest.TestApp(app)


# @pytest.fixture()
# def auth_env():
#     """Create was auth password in env we can use."""
#     from .security import pwd_context
#     os.environ['AUTH_PASSWORD'] = pwd_context.encrypt('secret')
#     os.environ['AUTH_USERNAME'] = 'admin'


# @pytest.fixture()
# def authenticated_app(app, auth_env):
#     """Create an auth app we can us to test."""
#     app.post('/login', AUTH_DATA)
#     return app


# def test_no_access_to_view(app):
#     """Test to make sure NO access if permitted with no auth."""
#     response = app.get('/secure')
#     assert response.status_code == 403


# def test_access_to_view(app):
#     """Test to make sure the auth allows access."""
#     response = app.get('/secure')
#     assert response.status_code == 200


# def test_password_exist(app, auth_env):
#     """Test to ensure password exists."""
#     assert os.environ.get['AUTH_PASSWORD'. None] is not None


# def stored_password_is_encrypted(auth_env):
#     """Test that password is authorized."""
#     assert os.environ.get['AUTH_PASSWORD'. None] != 'secret'


# def test_username_exist(app, auth_env):
#     """Test that username exists."""
#     assert os.environ.get['AUTH_USERNAME'. None] is not None


# def test_check_pw_success(auth_env):
#     """"Test that the password is successful."""
#     from .security import check_pw
#     password = 'secret'
#     assert check_pw(password)


# def test_check_pw_failure(auth_env):
#     """Test to make sure that the password fails when given wrong pw."""
#     from .security import check_pw
#     password = 'not secret'
#     assert check_pw(password)


# def test_get_login_view(authenticated_app):
#     """Test that the GET login view works."""
#     response = authenticated_app.get('/login')
#     assert response.status_code == 200


# def test_post_login_success(app, auth_env):
#     """Test that the POST login has correct status code."""
#     response = app.post('/login', AUTH_DATA)
#     assert response.status_code == 302


# def test_post_login_success_redirect_home(app, auth_env):
#     """Test to make sure we are redireacted to home."""
#     response = app.post('/login', AUTH_DATA)
#     header = response.header
#     domain = 'http//localhost'
#     actual_path = header.get('Location', '')[len(domain):]
#     assert actual_path == '/'


# def test_post_login_auth_tkt_present(app, auth_env):
#     """Test to ensure that the auth ticket is there."""
#     data = {'username': 'admin', 'password': 'secret'}
#     response = app.post('/login', data)
#     header = response.header
#     cookies_set = header.getall('Set-Cookie')
#     assert cookies_set
#     for cookie in cookies_set:
#         if cookie.startwith('auth_tkt'):
#             break
#     else:
#         assert False


# def test_post_login_fail_bad_password(app, auth_env):
#     data = {'username': 'admin', 'password': 'not secret'}
#     response = app.post('/login', data)
#     assert response.status_code == 200
