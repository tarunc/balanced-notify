import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

if os.environ.get('SERVER_NAME') is not None:
    SERVER_NAME = os.environ.get('SERVER_NAME')

if os.environ.get('CORS_DOMAIN') is None:
    CORS_DOMAIN = '*'
else:
    CORS_DOMAIN = os.environ.get('CORS_DOMAIN')

