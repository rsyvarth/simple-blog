"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views

from flask_restful import reqparse, abort, Api, Resource
api = Api(app)

## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/api/_ah/warmup', 'warmup', view_func=views.warmup)

# Login page
app.add_url_rule('/login', 'login', view_func=views.login)

# Home page
app.add_url_rule('/api/', 'home', view_func=views.home)

# Test page
app.add_url_rule('/api/test', 'test', view_func=views.test)



TODOS = {
    'todo1': {'id': 1, 'title': 'build an API'},
    'todo2': {'id': 2, 'title': '?????'},
    'todo3': {'id': 3, 'title': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/api/todos')
api.add_resource(Todo, '/api/todos/<todo_id>')





# # Say hello
# app.add_url_rule('/api/hello/<username>', 'say_hello', view_func=views.say_hello)

# # Examples list page
# app.add_url_rule('/api/examples', 'list_examples', view_func=views.list_examples, methods=['GET', 'POST'])

# # Examples list page (cached)
# app.add_url_rule('/api/examples/cached', 'cached_examples', view_func=views.cached_examples, methods=['GET'])

# # Contrived admin-only view example
# app.add_url_rule('/api/admin_only', 'admin_only', view_func=views.admin_only)

# # Edit an example
# app.add_url_rule('/api/examples/<int:example_id>/edit', 'edit_example', view_func=views.edit_example, methods=['GET', 'POST'])

# # Delete an example
# app.add_url_rule('/api/examples/<int:example_id>/delete', view_func=views.delete_example, methods=['POST'])


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

