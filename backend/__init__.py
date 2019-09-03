#!/usr/bin/env python3
# native imports
import os
import base64

# flask imports
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, set_access_cookies, set_refresh_cookies, unset_jwt_cookies

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'app.db'))
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres'):
    print("Using POSTGRES")
else:
    print("Using app.db...")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get(
    'RECIPEME_JWT_SECRET_KEY', 'changemepls')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# TODO change this to True once we test this
app.config['JWT_COOKIE_CSRF_PROTECT'] = False


# only if we're in prod, then use HTTPS only cookies
app.config['JWT_COOKIE_SECURE'] = os.environ.get('USE_SECURE_COOKIES', False)

# init the JWT manager
jwt = JWTManager(app)

# create the Api for endpoints (adding later)
api = Api(app)

# database
db = SQLAlchemy(app)
