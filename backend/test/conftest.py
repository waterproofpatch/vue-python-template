import pytest
import tempfile
import os

from backend import flask_app, db, app
from backend.models import User

from flask_jwt_extended import create_access_token, create_refresh_token


@pytest.fixture
def test_user():
    """
    A test database user
    """
    test_user = User(email='test@gmail.com', password='passwordpassword')
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
def authenticated_client(test_user, unauthenticated_client):
    """
    A client with valid access and refresh tokens, capable of authenticating 
    against endpoints guarded with @jwt_reqired
    """

    with unauthenticated_client.application.app_context():
        db.session.add(test_user)
        db.session.commit()

        access_token = create_access_token(identity='test@gmail.com')
        refresh_token = create_refresh_token(identity='test@gmail.com')
        unauthenticated_client.set_cookie(
            '/', 'access_token_cookie', access_token)
        unauthenticated_client.set_cookie(
            '/', 'refresh_token_cookie', refresh_token)
    yield unauthenticated_client
