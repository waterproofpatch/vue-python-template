
import io
import pytest
import re


def test_files_post(authenticated_client, unauthenticated_client):
    """Test files posting

    Arguments:
        authenticated_client {Client} -- client with tokens
        unauthenticated_client {Client} -- client without tokens
    """
    data = dict(
        theFile=(io.BytesIO(b'my file contents'), "valid.jpg"),
    )

    res = authenticated_client.post('/api/files',
                                    content_type='multipart/form-data', data=data)
    assert 200 == res.status_code


def test_files_post_invalid_filename(authenticated_client, unauthenticated_client):
    """Don't let us upload bins

    Arguments:
        authenticated_client {Client} -- client with tokens
        unauthenticated_client {Client} -- client without tokens
    """
    data = dict(
        theFile=(io.BytesIO(b'my file contents'), "valid.bin"),
    )

    res = authenticated_client.post('/api/files',
                                    content_type='multipart/form-data', data=data)
    assert 400 == res.status_code
    assert re.search(r'invalid filename', res.get_data().decode())
