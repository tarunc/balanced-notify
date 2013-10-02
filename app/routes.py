from app import app, db, models
from app.crossdomain import crossdomain
from app.models import Notification
from flask import request
from flask.ext.restless import APIManager
from sqlalchemy import and_
import simplejson as json

# Create the Flask-Restless API manager.
manager = APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Notification)

@app.route('/notifications', methods=['GET'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
def getNotifications():
    if not request.args['email']:
        return '', 404

    email = request.args.get('email')

    notifications = db.session.query(
        Notification.id,
        Notification.message).filter(
        and_(
            Notification.email == email,
            Notification.read == False)).all(
    )

    return json.dumps({'data': notifications})


@app.route('/notification', methods=['POST'])
def createNotifications():
    if not request.form['message'] or not request.form['email']:
        return 'Message and email required', 400

    message = str(request.form['message'])
    email = str(request.form['email'])
    # persistent = request.form.get('persistent', default=None)

    notification = Notification(
        message=message,
        email=email)
    db.session.add(notification)
    db.session.commit()

    return json.dumps({'data': notification})


@app.route('/notification/<int:notification_id>', methods=['DELETE'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
def markNotificationsAsRead(notification_id):
    existing_notification = Notification.query.get(notification_id)
    if not existing_notification:
        return '', 404

    existing_notification.read = True
    db.session.merge(existing_notification)
    db.session.commit()

    return 'ok';
