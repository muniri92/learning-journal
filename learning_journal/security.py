
from pyramid.security import Allow, Everyone, Authenticated
from pyramid.security import ALL_PERMISSIONS
from passlib.hash import sha256_crypt
import os


def check_password(pw):
    """Hash the password and save it."""
    hashed = os.environ.get('AUTH_PASSWORD', sha256_crypt.encrypt('muniri'))
    return sha256_crypt.verify(pw, hashed)


class DefaultRoot(object):
    """Create the DefaultRoot that is used in the __init__.py."""

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        """Instantiate that default root."""
        self.request = request


# from learning_journal.models import Entry
# class EntryRoot(object):

#     __name__ = 'entry'

#     @property
#     def __parent__(self):
#         return DefaultRoot(self.request)

#     def __init__(self, request):
#         self.request = request

#     def __getitem__(self, name):
#         entry_obj = Entry.by_id(name)
#         if entry_obj is None:
#             raise KeyError(name)
#         entry_obj.__parent__ = self
#         return entry_obj
