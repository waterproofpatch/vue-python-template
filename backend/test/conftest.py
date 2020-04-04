import pytest
import tempfile


from backend import create_app, create_api, create_db, create_jwt
from backend import app


@pytest.fixture
def client():
    # get a Flask app
    the_app = create_app()
    api = create_api(the_app)

    # db_fd, the_app.config['DATABASE'] = tempfile.mkstemp()
    the_app.config['TESTING'] = True
    print('fixture running')
    with the_app.test_client() as client:
        yield client
