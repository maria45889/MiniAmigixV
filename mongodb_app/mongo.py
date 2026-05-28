from django.conf import settings
from pymongo import MongoClient

_client = MongoClient(settings.MONGODB_SETTINGS["uri"])
db = _client[settings.MONGODB_SETTINGS['db']]
