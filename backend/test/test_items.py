import json

import pytest

from flask_jwt_extended import create_access_token, create_refresh_token


def test_get_items(authenticated_client):
    """
    Test the items endpoint, retreival
    """
    res = authenticated_client.get('/api/items')
    assert 200 == res.status_code
    assert 'application/json' == res.content_type

    # not expecting any items
    assert not res.get_json()


def test_get_items_fail_unauthenticated(unauthenticated_client):
    """
    Test the items endpoint, retreival
    """
    res = unauthenticated_client.get('/api/items')
    assert 401 == res.status_code


def test_post_items_fail_empty_payload(authenticated_client):
    """
    Test that items endpoint fails when json payload is empty
    """
    res = authenticated_client.post('/api/items', json={})
    assert 400 == res.status_code
    assert 'error' in res.json
    assert 'missing' in res.json['error']


def test_post_items_fail_content_type(authenticated_client):
    """
    Test that items endpoint fails when content type is wrong
    """
    res = authenticated_client.post('/api/items')
    assert 400 == res.status_code
    assert 'error' in res.json
    assert 'invalid content type' in res.json['error']


def test_delete_items_fail_unauthenticated(unauthenticated_client):
    """
    Test that items endpoint fails when we are not logged in and try to delete an item
    """
    res = unauthenticated_client.delete('/api/items?id=1')
    assert 401 == res.status_code


def test_post_items_fail_unauthenticated(unauthenticated_client):
    """
    Test that items endpoint fails when we are not logged in
    """
    res = unauthenticated_client.post('/api/items')
    assert 401 == res.status_code


def test_post_and_get_items_success(authenticated_client):
    """
    Test that we can add an item and retreive all of them
    """
    new_item = {'field1': 'field1_value', 'jsonfield1': {
        'key1': 'key1_value', 'list1': ['list1_value1', 'list1_value2']}}
    res = authenticated_client.post('api/items', json=new_item)
    assert res.status_code == 200

    res = authenticated_client.get('api/items')
    assert res.status_code == 200
    assert len(res.json) == 1
    assert 'field1' in res.json[0]
    assert res.json[0]['field1'] == 'field1_value'
    assert res.json[0]['owner'] == True

    new_item = {'field1': 'field1_value2', 'jsonfield1': {
        'key2': 'key2_value', 'list2': ['list2_value1', 'list2_value2']}}
    res = authenticated_client.post('api/items', json=new_item)
    assert res.status_code == 200

    res = authenticated_client.get('api/items')
    assert res.status_code == 200
    assert len(res.json) == 2
    assert 'field1' in res.json[1]
    assert res.json[1]['field1'] == 'field1_value2'
    assert res.json[1]['owner'] == True


def test_post_and_get_items_one_success(authenticated_client):
    """
    Test that we can add an item and then retreive it by id
    """
    new_item = {'field1': 'field1_value', 'jsonfield1': {
        'key1': 'key1_value', 'list1': ['list1_value1', 'list1_value2']}}
    res = authenticated_client.post('api/items', json=new_item)
    assert res.status_code == 200

    res = authenticated_client.get('api/items?id=1')
    assert res.status_code == 200
    assert len(res.json) == 1
    assert 'field1' in res.json[0]
    assert res.json[0]['field1'] == 'field1_value'
    assert res.json[0]['owner'] == True

    new_item = {'field1': 'field1_value2', 'jsonfield1': {
        'key2': 'key2_value', 'list2': ['list2_value1', 'list2_value2']}}
    res = authenticated_client.post('api/items', json=new_item)
    assert res.status_code == 200

    res = authenticated_client.get('api/items')
    assert res.status_code == 200
    assert len(res.json) == 2
    assert 'field1' in res.json[1]
    assert res.json[1]['field1'] == 'field1_value2'
    assert res.json[1]['owner'] == True


def test_delete_items_success(authenticated_client):
    """
    Test that we can delete an item
    """
    new_item = {'field1': 'field1_value', 'jsonfield1': {
        'key1': 'key1_value', 'list1': ['list1_value1', 'list1_value2']}}
    res = authenticated_client.post('api/items', json=new_item)
    assert res.status_code == 200

    res = authenticated_client.get('api/items')
    assert res.status_code == 200
    assert len(res.json) == 1
    assert 'field1' in res.json[0]
    assert res.json[0]['field1'] == 'field1_value'

    # try deleting wrong item, should fail
    res = authenticated_client.delete("api/items?id=2")
    assert res.status_code == 400
    assert 'error' in res.json
    assert 'Item not found' in res.json['error']

    # this one is legit
    res = authenticated_client.delete("api/items?id=1")
    assert res.status_code == 200

    res = authenticated_client.get('api/items')
    assert res.status_code == 200
    assert not res.json
