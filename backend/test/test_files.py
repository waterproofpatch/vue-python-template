
import pytest


def test_files_get(authenticated_client, unauthenticated_client):
    """
    <Description of the test>
    """
    res = authenticated_client.get('/api/items')
    assert 200 == res.status_code
    assert 'application/json' == res.content_type
