#!/usr/bin/env python3
"""
Item API backend. This is the main entry point for the app.
"""

# native imports
import os
import base64
import argparse
import bcrypt

# flask imports
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, set_access_cookies, set_refresh_cookies, unset_jwt_cookies

# my imports, some from __init__
from backend import jwt, api, app, db
from backend.models import Item, User, RevokedTokenModel

# globals
PASSWORD_MIN_LEN = 13


class Register(Resource):
    """
    Registration endpoint
    """

    def post(self):
        """
        Handle a registration request
        """
        if 'email' not in request.get_json():
            return {"error": "Must supply email address"}, 400
        if 'password' not in request.get_json():
            return {"error": "Must supply password"}, 400
        if 'passwordConfirmation' not in request.get_json():
            return {"error": "Must supply confirmation password"}, 400
        if request.get_json()['password'] != request.get_json()['passwordConfirmation']:
            return {"error": "Passwords don't match"}, 400
        if len(request.get_json()['password']) <= PASSWORD_MIN_LEN:
            return {"error": "Password must be > {} characters.".format(PASSWORD_MIN_LEN)}, 400
        if db.session.query(User.id).filter_by(email=request.get_json()['email']).scalar() is not None:
            return {"error": "Email is already registered."}, 400

        hashed_pw = User.generate_hash(
            plaintext_password=request.get_json()['password'].encode())
        new_user = User(email=request.get_json()['email'],
                        password=base64.b64encode(hashed_pw).decode())
        db.session.add(new_user)
        db.session.commit()

        # create tokens
        access_token = create_access_token(identity=new_user.email)
        refresh_token = create_refresh_token(identity=new_user.email)

        # set the cookies, at them to the response and return it
        resp = jsonify({'uid': new_user.id, 'email': new_user.email})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp


class Login(Resource):
    """
    Login endpoint
    """

    def post(self):
        """
        Handle a login request
        """
        if 'email' not in request.json:
            return {"error": "Must supply email address"}, 400
        if 'password' not in request.json:
            return {"error": "Must supply password"}, 400

        user = User.query.filter_by(email=request.json['email']).first()
        if user is None:
            return {"error": "Email or password incorrect"}, 400
        if bcrypt.hashpw(request.json['password'].encode(), base64.b64decode(user.password)) != base64.b64decode(user.password):
            return {"error": "Email or password incorrect"}, 400

        # create tokens
        resp = jsonify({'uid': user.id, 'email': user.email})
        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)

        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp


class Profile(Resource):
    """
    Profile endpoint
    """
    @jwt_required
    def get(self):
        """
        Handle a user getting their profile
        """
        user = User.query.filter_by(email=get_raw_jwt()['identity']).first()
        return {
            'email': user.email,
        }, 200

    # TODO may need fresh token
    @jwt_required
    def post(self):
        """
        Handle a user changing their information
        """
        if 'email' not in request.json:
            return {"error": "Must supply email address"}, 400
        if 'password' not in request.json:
            return {"error": "Must supply password"}, 400

        user = User.query.filter_by(email=get_raw_jwt()['identity']).first()
        if user is None:
            return {"error": "Email or password incorrect"}, 400
        if hashpw(request.json['password'].encode(), base64.b64decode(user.password)) != base64.b64decode(user.password):
            return {"error": "Email or password incorrect"}, 400
        if len(request.json['email']) == 0:
            return {"error": "Email must be at least one character"}, 400

        if request.json['email'] != user.email and db.session.query(User.id).filter_by(email=request.json['email']).scalar() is not None:
            return {"error": "Email is already registered."}, 400
        user.email = request.json['email']
        db.session.commit()
        return {'uid': user.id, 'email': user.email}, 200


class Items(Resource):
    """
    Items endpoint
    """
    @jwt_required
    def delete(self):
        """
        Deleting one of their items
        """
        item = Items.query.get(request.values['id'])
        if not item:
            return {"error": "Item not found."}, 400
        db.session.delete(item)
        db.session.commit()
        return {}, 200

    def get(self):
        """
        Get all items
        """
        if request.args.get('field1') is not None:
            return [x.as_json() for x in Item.query.filter(Item.name.contains(request.args.get('field1')))]
        return [x.as_json() for x in Item.query.all()], 200

    @jwt_required
    def put(self):
        """
        Update an existing item
        """
        item = Item.query.get(request.json['id'])
        item.field1 = request.json['field1']
        item.jsonfield1 = request.json['jsonfield1']
        db.session.commit()
        return [x.as_json() for x in Item.query.all()], 200

    @jwt_required
    def post(self):
        """
        Create a new item
        """
        user = User.query.filter_by(email=get_jwt_identity()).first()
        item = Item(field1=request.json['field1'],
                    jsonfield1=request.json['jsonfield1'],
                    user=user)
        db.session.add(item)
        db.session.commit()
        return [x.as_json() for x in Item.query.all()], 200


class TokenRefresh(Resource):
    """
    Refresh endpoint
    """
    @jwt_refresh_token_required
    def post(self):
        """
        Handle request for new access token
        """
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        # TODO id n/a?
        resp = jsonify({'id': 'n/a'})

        set_access_cookies(resp, access_token)
        return resp


class Logout(Resource):
    """
    Revoke the access token
    """
    @jwt_required
    def post(self):
        """
        Add the jti to the revoked token table
        """
        jti = get_raw_jwt()['jti']
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        resp = jsonify({'id': None})
        unset_jwt_cookies(resp)
        return resp


@jwt.token_in_blacklist_loader
def TokenCheckBlacklist(decrypted_token):
    """
    Check if a token is blacklisted
    """
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


@jwt.expired_token_loader
def TokenExpiredCallback(expired_token):
    """
    Tell the user their token expired
    """
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401


# endpoints here
api.add_resource(Items, '/api/items')
api.add_resource(Profile, '/api/profile')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')
api.add_resource(TokenRefresh, '/api/refresh')


def init_db(drop_all=False):
    """
    Initialize the database
    """
    print("Initializing DB")
    db.init_app(app)
    if drop_all:
        print("Dropping tables...")
        db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    """
    Entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dropall', action="store_true", required=False,
        help='drop tables in database before starting')
    args = parser.parse_args()

    init_db(drop_all=args.dropall)
    app.run(debug=True)
