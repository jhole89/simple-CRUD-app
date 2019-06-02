import json


def _helper_decode(bytes_data):
    return json.loads(bytes_data.decode('utf-8'))


def test_home(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is a valid index page
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"A simple CRUD web app example" in response.data


def test_get_all_contacts(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/contacts/' page is requested (GET)
    THEN check the response contains all contacts
    """
    expected_usernames = ('fry1999', 'simpo')
    all_users = test_client.get('/contacts/')
    data = _helper_decode(all_users.data)
    usernames = [data[i].get('username') for i in range(len(expected_usernames))]

    assert all_users.status_code == 200
    assert len(data) == len(expected_usernames)
    assert sorted(usernames) == sorted(expected_usernames)


def test_search_contact(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/contacts/search/<username>' page is requested (GET)
    THEN check the response contains a contact
    """
    fry = test_client.get('/contacts/search/fry1999')
    fry_data = _helper_decode(fry.data)

    assert fry.status_code == 200
    assert fry_data.get('username') == 'fry1999'
    assert fry_data.get('email') == 'fry@planet-express.com'
    assert fry_data.get('first_name') == 'Phillip'
    assert fry_data.get('surname') == 'Fry'

    unknown = test_client.get('/contacts/search/foobar')
    unknown_data = _helper_decode(unknown.data)

    assert unknown.status_code == 200
    assert unknown_data == {}


def test_create_contacts(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/contacts/create/' page is sent a payload (POST)
    THEN check the contact has been created
    """
    morty = dict(
        username='morty',
        email='morty@rickmanil.org',
        first_name='Morty',
        surname='Smith'
    )
    mimetype = 'application/json'

    response = test_client.post(
        '/contacts/create',
        data=json.dumps(morty),
        headers={'Content-Type': mimetype, 'Accept': mimetype}
    )

    data = _helper_decode(response.data)

    assert response.status_code == 200
    assert data.get('username') == morty.get('username')
    assert data.get('email') == morty.get('email')
    assert data.get('first_name') == morty.get('first_name')
    assert data.get('surname') == morty.get('surname')
    assert data.get('id') == 3


def test_update_contact(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/contacts/update/' page is sent a payload (POST)
    THEN check the contact has been updated
    """
    simpo = dict(
        username='simpo',
        email='chunkylover53@aol.com',
        first_name='Max',
        surname='Power'
    )
    mimetype = 'application/json'

    response = test_client.post(
        '/contacts/update',
        data=json.dumps(simpo),
        headers={'Content-Type': mimetype, 'Accept': mimetype}
    )

    data = _helper_decode(response.data)

    assert response.status_code == 200
    assert data.get('username') == simpo.get('username')
    assert data.get('email') == simpo.get('email')
    assert data.get('first_name') == simpo.get('first_name')
    assert data.get('surname') == simpo.get('surname')


def test_delete_contact(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/contacts/delete/<username' page is requested (DELETE)
    THEN check the contact has been removed
    """
    fry = test_client.delete('/contacts/delete/fry1999')
    search_fry = test_client.get('/contacts/search/fry1999')

    assert fry.status_code == 200
    assert _helper_decode(search_fry.data) == {}
