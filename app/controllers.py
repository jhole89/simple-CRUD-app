from typing import *

from flask import render_template, request, Response

from app import app, db
from app.models import Contact, ContactSchema

contact_schema = ContactSchema()


@app.route('/')
@app.route('/index', methods=['GET'])
def home():
    """
    API endpoint for home /
    :return: rendered index.html page
    """
    return render_template("index.html")


@app.route('/contacts')
@app.route('/contacts/', methods=['GET'])
def get_all_contacts() -> Any:
    """
    API endpoint for contacts/.
    :return: List of all Contacts serialized to JSON
    """
    contacts = Contact.query.all()
    return contact_schema.jsonify(contacts, many=True)


@app.route('/contacts/search/<string:username>', methods=['GET'])
def search_contact(username: str) -> Any:
    """
    API endpoint for contacts/search/<username>.  Searches by given username.
    :return: Contact serialized to JSON
    """
    return contact_schema.jsonify(Contact.query.filter_by(username=username).first())


@app.route('/contacts/create', methods=['POST'])
def create_contact() -> Any:
    """
    API endpoint for contacts/create.  Creates new contact by given username.
    :return: New contact serialized to JSON
    """

    body = request.get_json()

    contact = Contact(
        username=body.get('username'),
        email=body.get('email'),
        first_name=body.get('first_name'),
        surname=body.get('surname')
    )
    db.session.add(contact)
    db.session.commit()

    return contact_schema.jsonify(contact)


@app.route('/contacts/update', methods=['POST'])
def update_contact() -> Any:
    """
    API endpoint for contacts/update.  Updates existing contact by given username.
    :return: Contact serialized to JSON
    """
    body = request.get_json()
    contact = Contact.query.filter_by(username=body.get('username'))
    contact.update(body)

    db.session.commit()

    return contact_schema.jsonify(contact)


@app.route('/contacts/delete/<string:username>', methods=['DELETE'])
def delete_contact(username: str) -> Response:
    """
    API endpoint for contacts/delete/<username>.  Deletes existing contact by given username.
    :return: New contact serialized to JSON
    """
    Contact.query.filter_by(username=username).delete()
    db.session.commit()
    return Response(status=200)
