import pytest


def test_index(client):
    print('ok testing app')
    res = client.get('/index')
    print(res)
    assert True
