import pytest


def test_items(client):
    """
    Test the items endpoint
    """
    res = client.get('/api/items')
    assert 200 == res.status_code
    assert 'application/json' == res.content_type
    # not expecting any items
    assert not res.get_json()

    assert True
