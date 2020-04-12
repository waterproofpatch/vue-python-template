import pytest
import tempfile
import os

from backend import flask_app, app

from flask_jwt_extended import create_access_token, create_refresh_token


@pytest.fixture
def client():
    """
    A client with no access tokens.
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'test_app.db')
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    flask_app.config['TESTING'] = True

    app.init_db(test_data=True, drop_all=True)

    with flask_app.test_client() as client:
        yield client


@pytest.fixture()
def authenticated_client(client):
    """
    A client with valid access and refresh tokens, capable of authenticating 
    against endpoints garded with @jwt_reqired
    """

    with client.application.app_context():
        access_token = create_access_token(identity='test@gmail.com')
        refresh_token = create_refresh_token(identity='test@gmail.com')
        client.set_cookie('/', 'access_token_cookie', access_token)
        client.set_cookie('/', 'refresh_token_cookie', refresh_token)
    yield client
