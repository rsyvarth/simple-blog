"""
urls.py

URL dispatch route mappings and error handlers

"""

from google.appengine.datastore.datastore_query import Cursor

from flask import render_template

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application import app
from application import views

from models import EntryModel
from decorators import login_required, admin_required

import logging

from flask_restful import reqparse, abort, Api, Resource
api = Api(app)

## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/api/_ah/warmup', 'warmup', view_func=views.warmup)

# Login page
app.add_url_rule('/login', 'login', view_func=views.login)


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
            'added_by': {
                # 'email': entry.added_by.email(),
                'username': entry.added_by.nickname(),
                'user_id': entry.added_by.user_id()
            },
            'timestamp': entry.timestamp.isoformat(),
            'updated': entry.updated.isoformat()
        }


# EntryList
# shows a list of all entries, and lets you POST to add new entry
class EntryList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cursor')

        args = parser.parse_args()
        curs = Cursor(urlsafe=args['cursor'])

        entries, next_curs, more = EntryModel.query().order(-EntryModel.timestamp).fetch_page(1, start_cursor=curs)

        out = []
        for entry in entries:
            out.append(Entry.format(entry))

        nextCurs = ""
        if more:
            nextCurs = next_curs.urlsafe()

        return {
            'meta': {
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
api.add_resource(Entry, '/api/entries/<entry_id>')


