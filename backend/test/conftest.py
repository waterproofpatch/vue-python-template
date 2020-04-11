import pytest
import tempfile
import os

from backend import flask_app, app


@pytest.fixture
def client():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'test_app.db')
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    flask_app.config['TESTING'] = True

    app.init_db(test_data=True, drop_all=True)

    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def short_jwt_client():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'test_app.db')
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    flask_app.config['TESTING'] = True

    app.init_db(test_data=True, drop_all=True)

    with flask_app.test_client() as client:
        yield client
