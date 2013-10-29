from __future__ import unicode_literals
import os

from flask.ext.mongoengine import MongoEngine

import factory


app = factory.create_app(__name__, os.path.abspath(os.path.dirname(__file__)))
db = MongoEngine(app)


if __name__ == '__main__':
    app.run()