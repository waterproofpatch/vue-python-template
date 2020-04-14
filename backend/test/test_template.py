import json

import pytest

from flask_jwt_extended import create_access_token, create_refresh_token


def test_get_items(authenticated_client, unauthenticated_client):
    """
    <Description of the test>
    """
    assert authenticated_client is not None
    assert unauthenticated_client is not None
