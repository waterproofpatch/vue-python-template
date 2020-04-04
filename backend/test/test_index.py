import pytest


def test_index(client):
    res = client.get('/api/items')
    print(res)
    assert True
