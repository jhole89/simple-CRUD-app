from app import db, ma


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))

    def __repr__(self):
        return '<Email {}>'.format(self.email)


class EmailSchema(ma.ModelSchema):
    class Meta:
        model = Email


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.relationship('Email', backref="contact", cascade="all, delete-orphan", lazy='dynamic')
    first_name = db.Column(db.String(128))
    surname = db.Column(db.String(128))

    def __repr__(self):
        return '<Contact {}>'.format(self.username)


class ContactSchema(ma.ModelSchema):
    class Meta:
        model = Contact
