"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users, mail
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect, abort

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
# from forms import ExampleForm
# from models import ExampleModel
from models import EntryModel, EmailSubscriptionModel
import datetime

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


def home():
    return say_hello("Test");
    # return redirect(url_for('list_examples'))

def login():
    if not users.get_current_user():
        return redirect(users.create_login_url(request.url))

    subscription = EmailSubscriptionModel(
        user = users.get_current_user()
    )

    try:
        subscription.put()
        return redirect("");
    except CapabilityDisabledError:
        return {'status' : 500, 'message' : 'can\'t access database'}, 500
        

def logout():
    if users.get_current_user():
        return redirect(users.create_logout_url(request.url))
    return redirect("");

def test():
    return '{}';


def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username

def digest():
    sender_address = "Simple Blog <robert.syvarth@gmail.com>"
    subject = "Simple Blog - Daily Digest"

    body = """
This is a digest email.
"""
    entries = EntryModel.query(EntryModel.timestamp > (datetime.datetime.now() + datetime.timedelta(days=-1))).order(-EntryModel.timestamp)
    for entry in entries:
        body = body + """
    %s
     - %s
""" % (entry.title, "http://simpleblog-1082.appspot.com/post/" + str(entry.key.id()))

    body = body + """

That is all!
"""

    subs = EmailSubscriptionModel.query(EmailSubscriptionModel.subscribed == True)
    for sub in subs:
        mail.send_mail(sender_address, sub.user.email(), subject, body)

    return ""


# @login_required
# def list_examples():
#     """List all examples"""
#     examples = ExampleModel.query()
#     form = ExampleForm()
#     if form.validate_on_submit():
#         example = ExampleModel(
#             example_name=form.example_name.data,
#             example_description=form.example_description.data,
#             added_by=users.get_current_user()
#         )
#         try:
#             example.put()
#             example_id = example.key.id()
#             flash(u'Example %s successfully saved.' % example_id, 'success')
#             return redirect(url_for('list_examples'))
#         except CapabilityDisabledError:
#             flash(u'App Engine Datastore is currently in read-only mode.', 'info')
#             return redirect(url_for('list_examples'))
#     return render_template('list_examples.html', examples=examples, form=form)


# @login_required
# def edit_example(example_id):
#     example = ExampleModel.get_by_id(example_id)
#     form = ExampleForm(obj=example)
#     if request.method == "POST":
#         if form.validate_on_submit():
#             example.example_name = form.data.get('example_name')
#             example.example_description = form.data.get('example_description')
#             example.put()
#             flash(u'Example %s successfully saved.' % example_id, 'success')
#             return redirect(url_for('list_examples'))
#     return render_template('edit_example.html', example=example, form=form)


# @login_required
# def delete_example(example_id):
#     """Delete an example object"""
#     example = ExampleModel.get_by_id(example_id)
#     if request.method == "POST":
#         try:
#             example.key.delete()
#             flash(u'Example %s successfully deleted.' % example_id, 'success')
#             return redirect(url_for('list_examples'))
#         except CapabilityDisabledError:
#             flash(u'App Engine Datastore is currently in read-only mode.', 'info')
#             return redirect(url_for('list_examples'))


# @admin_required
# def admin_only():
#     """This view requires an admin account"""
#     return 'Super-seekrit admin page.'


# @cache.cached(timeout=60)
# def cached_examples():
#     """This view should be cached for 60 sec"""
#     examples = ExampleModel.query()
#     return render_template('list_examples_cached.html', examples=examples)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

