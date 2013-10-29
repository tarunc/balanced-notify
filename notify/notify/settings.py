import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = '~you-will-never-guess~'

#if os.environ.get('DATABASE_URL') is None:
#    MONGO_DATABASE_URI = 'mongodb://balanced:mysupersecretpassword123~`\
#        @paulo.mongohq.com:10045/notify'
#else:
#    MONGO_DATABASE_URI = os.environ['DATABASE_URL']
#
#if os.environ.get('DATABASE_NAME') is None:
#    DATABASE_NAME = 'notify'
#else:
#    DATABASE_NAME = os.environ['DATABASE_NAME']
#
## slow database query threshold (in seconds)
#DATABASE_QUERY_TIMEOUT = 0.5
#
#if os.environ.get('SERVER_NAME') is not None:
#    SERVER_NAME = os.environ.get('SERVER_NAME')
#
#if os.environ.get('CORS_DOMAIN') is None:
#    CORS_DOMAIN = '*'
#else:
#    CORS_DOMAIN = os.environ.get('CORS_DOMAIN')


MONGODB_SETTINGS = {
    'DB': 'notify',
}