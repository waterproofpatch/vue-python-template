import json
import datetime
import time

import pytest

from flask_jwt_extended import decode_token
import jwt


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
            if value.startswith('access_token_cookie'):
                token = value.split('=')[1].split(';')[0]
                decoded_token = decode_token(token)
                assert decoded_token['identity'] == 'test@gmail.com'
                assert decoded_token['type'] == 'access'
                assert decoded_token['fresh'] == False
            assert 'HttpOnly' in [x.strip() for x in value.split(';')]


def test_post_login_success_shortlived_token(client):
    """
    Test that we can login, but that within 1 second we have an expired token
    """
    client.application.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1  # one second!
    client.application.config['JWT_REFRESH_TOKEN_EXPIRES'] = 1  # one second!

    res = client.post(
        '/api/login',
        json={'email': 'test@gmail.com', 'password': 'passwordpassword'})
    assert 200 == res.status_code
    assert 'Set-Cookie' in res.headers
    assert res.headers['Set-Cookie'].startswith('access_token_cookie'.lower())
    assert 'email' in res.json and res.json['email'] == 'test@gmail.com'
    assert 'uid' in res.json and res.json['uid'] == 1

    access_token = None
    refresh_token = None
    for key, value in res.headers:
        if key == 'Set-Cookie':
            assert value.startswith('access_token_cookie') or value.startswith(
                'refresh_token_cookie')
            if value.startswith('refresh_token_cookie'):
                token = value.split('=')[1].split(';')[0]
                refresh_token = token
                decoded_token = decode_token(token)
                assert decoded_token['identity'] == 'test@gmail.com'
                assert decoded_token['type'] == 'refresh'
                assert 'HttpOnly' in [x.strip() for x in value.split(';')]
            if value.startswith('access_token_cookie'):
                token = value.split('=')[1].split(';')[0]
                access_token = token
                decoded_token = decode_token(token)
                assert decoded_token['identity'] == 'test@gmail.com'
                assert decoded_token['type'] == 'access'
                assert decoded_token['fresh'] == False
                assert 'HttpOnly' in [x.strip() for x in value.split(';')]

    # wait for token to expire!
    time.sleep(2)
    for token in [access_token, refresh_token]:
        expired = False
        try:
            decoded_token = decode_token(token)
        except jwt.exceptions.ExpiredSignatureError:
            expired = True
        finally:
            assert expired
