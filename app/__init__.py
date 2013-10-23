import os

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('app.settings.default')
if os.getenv('BALANCED_ENV'):
    app.config.from_object('app.settings.' + os.getenv('BALANCED_ENV'))

mongoClient = MongoClient(app.config.get('MONGO_DATABASE_URI'))
db = mongoClient[app.config.get('DATABASE_NAME')]


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        '/tmp/notification.log',
        'a',
        1 * 1024 * 1024,
        10)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s:\
            %(message)s[%(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('notification startup')

from app import routes

if __name__ == '__main__':
    app.run()
