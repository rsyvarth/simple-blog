"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class EntryModel(ndb.Model):
    """Entry Model"""
    title = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)


class EmailSubscriptionModel(ndb.Model):
    """Email Subscription Model"""
    user = ndb.UserProperty()
    subscribed = ndb.BooleanProperty(default=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
