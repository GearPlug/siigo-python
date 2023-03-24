import requests

from siigo.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):

    def __init__(self, access_key):
        pass