#!/usr/bin/env python3
# native imports
import os

# flask imports
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# from backend import auth

basedir = os.path.abspath(os.path.dirname(__file__))


def create_db(app):
    # database
    db = SQLAlchemy(app)
    return db


def create_api(app):
    # create the Api for endpoints (adding later)
    api = Api(app)
    return api


def create_jwt(app):
    # init the JWT manager
    jwt = JWTManager(app)
    return jwt


def create_app():
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
    app.config['JWT_COOKIE_SECURE'] = os.environ.get(
        'USE_SECURE_COOKIES', False)

    return app


# initialize the app etc
app = create_app()
db = create_db(app)
api = create_api(app)
jwt = create_jwt(app)

# add the endpoints
# api.add_resource(auth.Profile, '/api/profile')
# api.add_resource(auth.Register, '/api/register')
# api.add_resource(auth.Login, '/api/login')
# api.add_resource(auth.Logout, '/api/logout')
# api.add_resource(auth.TokenRefresh, '/api/refresh')
# api.add_resource(auth.Items, '/api/items')
