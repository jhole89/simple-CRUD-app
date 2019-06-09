import pytest

from app import create_app, db
from app.models import Contact, Email
from test.config import TestConfig


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestConfig)
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    simpo_email = Email(email='chunkylover53@aol.com')
    simpo = Contact(
        username='simpo',
        email=[simpo_email],
        first_name='Homer',
        surname='Simpson'
    )

    fry_email = Email(email='fry@planet-express.com')
    fry = Contact(
        username='fry1999',
        email=[fry_email],
        first_name='Phillip',
        surname='Fry'
    )
    db.session.add(simpo)
    db.session.add(simpo_email)

    db.session.add(fry)
    db.session.add(fry_email)

    db.session.commit()

    yield db
    db.drop_all()
