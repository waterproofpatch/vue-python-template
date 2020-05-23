
import io
import pytest


def test_files_get(authenticated_client, unauthenticated_client):
    """
    <Description of the test>
    """
    data = dict(
        theFile=(io.BytesIO(b'my file contents'), "valid.jpg"),
    )

    res = authenticated_client.post('/api/files',
                                    content_type='multipart/form-data', data=data)
    assert 200 == res.status_code
