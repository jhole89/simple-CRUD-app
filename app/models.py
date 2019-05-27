from app import db


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(128))
    surname = db.Column(db.String(128))

    def __repr__(self):
        return '<Contact {}>'.format(self.username)
