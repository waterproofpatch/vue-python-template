import json

import pytest


def test_post_login_wrong_email(client):
    """
    Test that we handle wrong email properly
    """
    res = client.post(
        '/api/login',
        json={'email': 'test@gmail.comwrong', 'password': 'passwordpassword'})
    assert 401 == res.status_code
    assert 'Set-Cookie' not in res.headers


def test_post_login_wrong_password(client):
    """
    Test that we handle wrong password properly
    """
    res = client.post(
        '/api/login',
        json={'email': 'test@gmail.com', 'password': 'passwordpasswordwrong'})
    assert 401 == res.status_code
    assert 'Set-Cookie' not in res.headers


def test_post_login_missing_email(client):
    """
    Test that we handle missing email properly
    """
    res = client.post(
        '/api/login',
        json={'password': 'passwordpassword'})
    assert 400 == res.status_code
    assert 'Set-Cookie' not in res.headers


def test_post_login_missing_password(client):
    """
    Test that we handle missing password properly
    """
    res = client.post(
        '/api/login',
        json={'email': 'test@gmail.com'})
    assert 400 == res.status_code
    assert 'Set-Cookie' not in res.headers


def test_post_login_success(client):
    """
    Test that we can login
    """
    res = client.post(
        '/api/login',
        json={'email': 'test@gmail.com', 'password': 'passwordpassword'})
    assert 200 == res.status_code
    assert 'Set-Cookie' in res.headers
    assert res.headers['Set-Cookie'].startswith('access_token_cookie'.lower())
    assert 'email' in res.json and res.json['email'] == 'test@gmail.com'
    assert 'uid' in res.json and res.json['uid'] == 1
    for key, value in res.headers:
        if key == 'Set-Cookie':
            assert value.startswith('access_token_cookie') or value.startswith(
                'refresh_token_cookie')
            assert 'HttpOnly' in [x.strip() for x in value.split(';')]
