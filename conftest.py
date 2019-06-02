import pytest

from app import create_app, db
from app.models import Contact
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

    simpo = Contact(
        username='simpo',
        email='chunkylover53@aol.com',
        first_name='Homer',
        surname='Simpson'
    )
    fry = Contact(
        username='fry1999',
        email='fry@planet-express.com',
        first_name='Phillip',
        surname='Fry'
    )
    db.session.add(simpo)
    db.session.add(fry)

    db.session.commit()

    yield db
    db.drop_all()
