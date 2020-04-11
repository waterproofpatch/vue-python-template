import json

import pytest


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


def test_post_items(client):
    """
    Test that we must authenticate to add an item
    """
    res = client.post('/api/items')
    # we haven't logged in
    assert 401 == res.status_code

    res = client.post(
        '/api/login',
        json={'email': 'test@gmail.com', 'password': 'passwordpassword'})
    assert 200 == res.status_code

    # res = client.post('/api/items')
    # # we haven't logged in
    # assert 200 == res.status_code
