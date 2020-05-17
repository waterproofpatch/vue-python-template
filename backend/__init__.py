#!/usr/bin/env python3
# native imports
import os

# flask imports
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

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
        print('Using posgress')
    else:
        print('Using sqlite')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = "uploads"
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 megs
    app.config['JWT_SECRET_KEY'] = os.environ.get(
        'TEMPLATE_JWT_SECRET_KEY', 'changemepls')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 15  # fifteen minutes
    # app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 60 * 60 * 24 * 30  # 30 days
    # TODO change this to True once we test this
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    # only if we're in prod, then use HTTPS only cookies
    app.config['JWT_COOKIE_SECURE'] = os.environ.get(
        'USE_SECURE_COOKIES', False)

    # create location for file uploads
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])

    return app


# initialize the app etc
flask_app = create_app()
db = create_db(flask_app)
api = create_api(flask_app)
jwt = create_jwt(flask_app)
