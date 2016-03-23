
from pyramid.security import Allow, Everyone, Authenticated
from pyramid.security import ALL_PERMISSIONS
# from learning_journal.models import Entry
from passlib.hash import sha256_crypt
import os


def check_password(pw):
    """Hash the password and save it."""
    hashed = os.environ.get('AUTH_PASSWORD', sha256_crypt.encrypt('muniri'))
    return sha256_crypt.verify(pw, hashed)


class DefaultRoot(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, ALL_PERMISSIONS),
    ]


    def __init__(self, request):
        self.request = request


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
