import json
import datetime
import time

import pytest

from flask_jwt_extended import decode_token
import jwt

from backend import db


def test_post_login_wrong_email(unauthenticated_client):
    """
    Test that we handle wrong email properly
    """
    res = unauthenticated_client.post(
        '/api/login',
        json={'email': 'test1@gmail.comwrong', 'password': 'passwordpassword1'})
    assert 401 == res.status_code
    assert 'Set-Cookie' not in res.headers


def test_post_login_wrong_password(unauthenticated_client):
    """
    Test that we handle wrong password properly
    """
    res = unauthenticated_client.post(
        '/api/login',
        json={'email': 'test1@gmail.com', 'password': 'passwordpassword1wrong'})
    assert 401 == res.status_code
    assert 'Set-Cookie' not in res.headers


def test_post_login_missing_email(unauthenticated_client):
    """
    Test that we handle missing email properly
    """
    res = unauthenticated_client.post(
        '/api/login',
        json={'password': 'passwordpassword1'})
    assert 400 == res.status_code
    assert 'Set-Cookie' not in res.headers


def test_post_login_missing_password(unauthenticated_client):
    """
    Test that we handle missing password properly
    """
    res = unauthenticated_client.post(
        '/api/login',
        json={'email': 'test1@gmail.com'})
    assert 400 == res.status_code
    assert 'Set-Cookie' not in res.headers


def test_post_login_success(unauthenticated_client, test_user_1):
    """
    Test that we can login
    """
    with unauthenticated_client.application.app_context():
        db.session.add(test_user_1)
        db.session.commit()

    res = unauthenticated_client.post(
        '/api/login',
        json={'email': 'test1@gmail.com', 'password': 'passwordpassword1'})
    assert 200 == res.status_code
    assert 'Set-Cookie' in res.headers
    assert res.headers['Set-Cookie'].startswith('access_token_cookie'.lower())
    assert 'email' in res.json and res.json['email'] == 'test1@gmail.com'
    assert 'uid' in res.json and res.json['uid'] == 1
    for key, value in res.headers:
        if key == 'Set-Cookie':
            assert value.startswith('access_token_cookie') or value.startswith(
                'refresh_token_cookie')
            if value.startswith('access_token_cookie'):
                token = value.split('=')[1].split(';')[0]
                decoded_token = decode_token(token)
                assert decoded_token['identity'] == 'test1@gmail.com'
                assert decoded_token['type'] == 'access'
                assert decoded_token['fresh'] == False
            assert 'HttpOnly' in [x.strip() for x in value.split(';')]


def test_post_login_success_shortlived_token(unauthenticated_client, test_user_1):
    """
    Test that we can login, but that within 1 second we have an expired token
    """
    unauthenticated_client.application.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1  # one second!
    # one second!
    unauthenticated_client.application.config['JWT_REFRESH_TOKEN_EXPIRES'] = 1

    with unauthenticated_client.application.app_context():
        db.session.add(test_user_1)
        db.session.commit()

    res = unauthenticated_client.post(
        '/api/login',
        json={'email': 'test1@gmail.com', 'password': 'passwordpassword1'})
    assert 200 == res.status_code
    assert 'Set-Cookie' in res.headers
    assert res.headers['Set-Cookie'].startswith('access_token_cookie'.lower())
    assert 'email' in res.json and res.json['email'] == 'test1@gmail.com'
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
                assert decoded_token['identity'] == 'test1@gmail.com'
                assert decoded_token['type'] == 'refresh'
                assert 'HttpOnly' in [x.strip() for x in value.split(';')]
            if value.startswith('access_token_cookie'):
                token = value.split('=')[1].split(';')[0]
                access_token = token
                decoded_token = decode_token(token)
                assert decoded_token['identity'] == 'test1@gmail.com'
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
