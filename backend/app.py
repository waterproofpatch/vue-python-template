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
from backend import auth  # for our authentication endpoints


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


# endpoints here
api.add_resource(Items, '/api/items')


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
