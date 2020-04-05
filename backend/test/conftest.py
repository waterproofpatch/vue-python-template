import pytest
import tempfile

from backend import flask_app, app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    print('fixture running')
    with flask_app.test_client() as client:
        yield client
