
from flask import render_template, request, Response

from app import db, app
from app.models import Contact, ContactSchema, Email

contact_schema = ContactSchema()


@app.route('/')
@app.route('/index', methods=['GET'])
def home():
    """
    API endpoint for home /
    :return: rendered index.html page
    """
    return render_template("index.html")


@app.route('/contacts/search/<string:username>', methods=['GET'])
def search_contact(username: str) -> Response:
    """
    API endpoint for contacts/search/<username>.  Searches by given username.
    :return: Contact serialized to JSON
    """
    return contact_schema.jsonify(Contact.query.filter_by(username=username).first())


@app.route('/contacts/create', methods=['POST'])
def create_contact() -> Response:
    """
    API endpoint for contacts/create.  Creates new contact by given username.
    :return: New contact serialized to JSON
    """

    body = request.get_json()
    emails = body.get('email')
    if not isinstance(emails, list):
        email_list = list(body.get('email'))
    else:
        email_list = emails

    email_entities = [Email(email=email) for email in email_list]

    contact = Contact(
        username=body.get('username'),
        email=email_entities,
        first_name=body.get('first_name'),
        surname=body.get('surname')
    )

    db.session.add(contact)
    for email in email_entities:
        db.session.add(email)

    db.session.commit()

    return contact_schema.jsonify(contact)


@app.route('/contacts/update', methods=['POST'])
def update_contact() -> Response:
    """
    API endpoint for contacts/update.  Updates existing contact by given username.
    :return: Contact serialized to JSON
    """
    body = request.get_json()
    contact = Contact.query.filter_by(username=body.get('username')).first()

    for email in contact.email:
        db.session.delete(email)

    db.session.commit()

    emails = body.get('email')
    if not isinstance(emails, list):
        email_list = list(body.get('email'))
    else:
        email_list = emails

    email_entities = [Email(email=email) for email in email_list]
    for email in email_entities:
        db.session.add(email)

    contact.username = body.get('username')
    contact.first_name = body.get('first_name')
    contact.surname = body.get('surname')
    contact.email = email_entities

    db.session.commit()

    return contact_schema.jsonify(Contact.query.filter_by(username=body.get('username')).first())


@app.route('/contacts/delete/<string:username>', methods=['DELETE'])
def delete_contact(username: str) -> Response:
    """
    API endpoint for contacts/delete/<username>.  Deletes existing contact by given username.
    :return: New contact serialized to JSON
    """
    Contact.query.filter_by(username=username).delete()
    db.session.commit()
    return Response(status=200)
