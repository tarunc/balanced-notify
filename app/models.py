from app import db

# Notification model
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, nullable=True)
    message = db.Column(db.String(255), index=True, nullable=False)
    read = db.Column(db.Boolean, default=False)
    # persistent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now())
    expires_at = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def _asdict(self):
        return {'id': self.id, 'message': self.message}

# Create the database tables.
db.create_all()
