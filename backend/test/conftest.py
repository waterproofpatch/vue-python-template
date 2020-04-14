import pytest
import tempfile
import os

from backend import flask_app, db, app
from backend.models import User, Item

from flask_jwt_extended import create_access_token, create_refresh_token

from backend.models import User, Item
from backend import db


@pytest.fixture
def test_user_2():
    """
    A test database user
    """
    test_user = User(email='test2@gmail.com', password='passwordpassword2')
    yield test_user


@pytest.fixture
def test_user_1():
    """
    A test database user
    """
    test_user = User(email='test1@gmail.com', password='passwordpassword1')
    yield test_user


@pytest.fixture
def unauthenticated_client():
    """
    A client with no access tokens.
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'test_app.db')
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    flask_app.config['TESTING'] = True

    app.init_db(db, drop_all=True)

    with flask_app.test_client() as client:
        yield client


@pytest.fixture()
def authenticated_client(test_user_1, test_user_2, unauthenticated_client):
    """
    A client with valid access and refresh tokens, capable of authenticating
    against endpoints guarded with @jwt_reqired
    """

    with unauthenticated_client.application.app_context():
        db.session.add(test_user_1)
        db.session.add(test_user_2)
        db.session.commit()

        # we'll authenticate as test1
        access_token = create_access_token(identity='test1@gmail.com')
        refresh_token = create_refresh_token(identity='test1@gmail.com')
        unauthenticated_client.set_cookie(
            '/', 'access_token_cookie', access_token)
        unauthenticated_client.set_cookie(
            '/', 'refresh_token_cookie', refresh_token)
    yield unauthenticated_client


@pytest.fixture()
def test_item(authenticated_client, test_user_1):
    item = Item(field1='field1_value',
                jsonfield1={'key': 'value'},
                user=test_user_1)
    with authenticated_client.application.app_context():
        db.session.add(item)
        db.session.commit()
