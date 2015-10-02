"""
urls.py

URL dispatch route mappings and error handlers

"""

from google.appengine.datastore.datastore_query import Cursor

from flask import render_template
from flask.ext.cors import CORS

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application import app
from application import views

from models import EntryModel, EmailSubscriptionModel
from decorators import login_required, admin_required

import logging

from flask_restful import reqparse, abort, Api, Resource
api = Api(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:1234"}})

## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/api/_ah/warmup', 'warmup', view_func=views.warmup)

# Login page
app.add_url_rule('/login', 'login', view_func=views.login)
app.add_url_rule('/logout', 'logout', view_func=views.logout)

# Run daily email digest
app.add_url_rule('/digest', 'digest', view_func=views.digest)


# Entry
# shows a single entry item and lets you delete a entry item
class Entry(Resource):
    def get(self, entry_id):
        entry = EntryModel.get_by_id(int(entry_id))
        if entry is None:
            return {'status' : 404, 'message' : 'entry not found'}, 404

        return Entry.format(entry), 200

    def delete(self, entry_id):
        logging.info("test")
        entry = EntryModel.get_by_id(int(entry_id))
        if entry is None:
            return {'status' : 404, 'message' : 'entry not found'}, 404
        entry.delete()
        return '', 204

    def put(self, entry_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('description')

        args = parser.parse_args()
        entry = EntryModel.get_by_id(int(entry_id))
        if entry is None:
            return {'status' : 404, 'message' : 'entry not found'}, 404

        entry.title = args['title']
        entry.description = args['description']

        try:
            entry.put()
            return Entry.format(entry), 201
        except CapabilityDisabledError:
            return {'status' : 500, 'message' : 'can\'t access database'}, 500

    @staticmethod
    def format(entry):
        if entry is None or entry.timestamp is None:
            return {}

        return {
            # 'id': entry.key.urlsafe(),
            'id': entry.key.id(),
            'title': entry.title,
            'description': entry.description,
            'added_by': UserSelf.format(entry.added_by, None),
            'timestamp': entry.timestamp.isoformat(),
            'updated': entry.updated.isoformat()
        }

api.add_resource(Entry, '/api/entries/<entry_id>')

# EntryList
# shows a list of all entries, and lets you POST to add new entry
class EntryList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cursor')

        args = parser.parse_args()
        curs = Cursor(urlsafe=args['cursor'])

        q = EntryModel.query()
        q_forward = q.order(-EntryModel.timestamp)
        q_reverse = q.order(EntryModel.timestamp)

        entries, next_curs, more = q_forward.fetch_page(10, start_cursor=curs)


        out = []
        for entry in entries:
            out.append(Entry.format(entry))

        nextCurs = ""
        if more:
            nextCurs = next_curs.urlsafe()

        prevCurs = ""
        if next_curs is not None:
            rev_cursor = next_curs.reversed()
            old_entries, prev_cursor, fewer = q_reverse.fetch_page(10, start_cursor=rev_cursor, offset=len(out))
            if prev_cursor is not None:
                prevCurs = prev_cursor.urlsafe()

        return {
            'meta': {
                'prev_curs': prevCurs,
                'curs': curs.urlsafe(), 
                'next_curs': nextCurs
            },
            'entries': out
        }

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('description')

        args = parser.parse_args()
        entry = EntryModel(
            title = args['title'],
            description = args['description'],
            added_by = users.get_current_user()
        )

        try:
            entry.put()
            return Entry.format(entry), 201

        except CapabilityDisabledError:
            return {'status' : 500, 'message' : 'can\'t access database'}, 500

##
## Actually setup the Api resource routing here
##
api.add_resource(EntryList, '/api/entries')



# UserSelf
# gets information about the current user
class UserSelf(Resource):
    def get(self):
        sub = EmailSubscriptionModel.query(EmailSubscriptionModel.user == users.get_current_user()).get()
        return self.format(users.get_current_user(), sub)

    @login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('subscribed', type=bool)
        args = parser.parse_args()

        sub = EmailSubscriptionModel.query(EmailSubscriptionModel.user == users.get_current_user()).get()
        sub.subscribed = args['subscribed']

        try:
            sub.put()
            return self.format(users.get_current_user(), sub)
        except CapabilityDisabledError:
            return {'status' : 500, 'message' : 'can\'t access database'}, 500

    @staticmethod
    def format(user, sub):
        if user is None:
            return {}

        return {
            # 'email': user.email(),
            'username': user.nickname(),
            'user_id': user.user_id(),
            'subscribed': sub.subscribed if sub is not None else False
        }


##
## Actually setup the Api resource routing here
##
api.add_resource(UserSelf, '/api/users/self')

