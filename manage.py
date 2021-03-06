from flask.ext.script import Manager, Server
from flask_debugtoolbar import DebugToolbarExtension
import os
import sys
if sys.argv[1] == 'test' or sys.argv[1] == 'coverage':
    os.environ['TESTING'] = 'true'

from inquizition import app
import inquizition.settings as settings

app.debug = settings.debug
app.config['SECRET_KEY'] = settings.secret_key

toolbar = DebugToolbarExtension(app)


manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0'))


@manager.command
def gunicorn():
    "Runs this with gunicorn (Production server)"
    import subprocess
    subprocess.call(['./scripts/gunicorn.sh'])


@manager.command
def tornado():
    "Runs this with tornado (Super non-blocking server)"
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from inquizition import app

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8000)
    IOLoop.instance().start()


@manager.command
def init_db():
    "Sets up the DB"
    print "Setting up DB"
    from inquizition.database import init_db
    init_db()


@manager.command
def dummy_db():
    "Adds dummy questions to the DB"
    print "Generating 100 questions for the DB"
    from inquizition.helpers import gen_dummy_data
    gen_dummy_data()


@manager.command
def load_db():
    "Loads questions from csv to the DB"
    print "Loading CSV into DB"
    from inquizition.helpers import load_questions
    load_questions()


@manager.command
def clear_db():
    "Clears the DB"
    print "Clearing DB"
    from inquizition.database import clear_db
    clear_db()


@manager.command
def purge_db():
    "Purges DB of old quizzes"
    print "Purging DB of old quizzes"
    from inquizition.database import purge_db
    purge_db()


@manager.command
def test():
    import subprocess
    result = subprocess.call(['nosetests'])
    return result
    


@manager.command
def coverage():
    import subprocess
    result = subprocess.call(['nosetests', '--with-coverage', '--cover-erase', '--cover-package=inquizition', '--cover-html'])
    return result

if __name__ == "__main__":
    manager.run()
