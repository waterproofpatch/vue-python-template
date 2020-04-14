
import pytest


def test_template(authenticated_client, unauthenticated_client):
    """
    <Description of the test>
    """
    assert authenticated_client is not None
    assert unauthenticated_client is not None
