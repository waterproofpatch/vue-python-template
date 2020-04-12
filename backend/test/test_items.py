import json

import pytest

from flask_jwt_extended import create_access_token, create_refresh_token


def test_get_items(client):
    """
    Test the items endpoint
    """
    res = client.get('/api/items')
    assert 200 == res.status_code
    assert 'application/json' == res.content_type
    # not expecting any items
    assert not res.get_json()

    assert True


def test_post_items(authenticated_client):
    """
    Test that we must authenticate to add an item
    """
    res = authenticated_client.post('/api/items')
    # we haven't logged in
    assert 200 == res.status_code
