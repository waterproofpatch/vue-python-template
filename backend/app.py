#!/usr/bin/env python3
"""
Item API backend. This is the main entry point for the app.

UWSGI: module: app(.py), callable: app
"""

# native imports
from backend.models import Item, User
import sys
import base64
import argparse

# flask imports
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# my imports, some from __init__
from backend import flask_app, db, api, views


print('registering endpoints')
api.add_resource(views.Profile, '/api/profile')
api.add_resource(views.Register, '/api/register')
api.add_resource(views.Login, '/api/login')
api.add_resource(views.Logout, '/api/logout')
api.add_resource(views.TokenRefresh, '/api/refresh')
api.add_resource(views.Items, '/api/items')


def init_db(test_data=False, drop_all=False):
    """
    Initialize the database
    """
    print("Initializing DB")
    db.init_app(flask_app)
    if drop_all:
        print("Dropping tables...")
        db.drop_all()
    db.create_all()
    if test_data:
        print("Adding test data...")
        hashed_pw = User.generate_hash(
            plaintext_password='passwordpassword'.encode())
        test_user = User(email='test@gmail.com',
                         password=base64.b64encode(hashed_pw))
        db.session.add(test_user)
        db.session.commit()
    db.session.commit()


if __name__ == "__main__":
    """
    Entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--dropall', action="store_true", required=False,
                        help='drop tables in database before starting')
    parser.add_argument('--testdata', action="store_true", required=False,
                        help='create some test data')
    parser.add_argument('--init', action="store_true", required=False,
                        help='just init database and do nothing else')
    args = parser.parse_args()

    if args.init:
        init_db(test_data=args.testdata, drop_all=args.dropall)
        sys.exit(0)
    init_db(test_data=args.testdata, drop_all=args.dropall)

    flask_app.run(debug=True)
