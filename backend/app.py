#!/usr/bin/env python3
"""
Item API backend. This is the main entry point for the app.

UWSGI: module: app(.py), callable: app
"""

# native imports
import sys
import base64
import argparse

# flask imports
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# my imports, some from __init__
from backend import flask_app, api, views, db


api.add_resource(views.Profile, '/api/profile')
api.add_resource(views.Register, '/api/register')
api.add_resource(views.Login, '/api/login')
api.add_resource(views.Logout, '/api/logout')
api.add_resource(views.TokenRefresh, '/api/refresh')
api.add_resource(views.Items, '/api/items')
# api.add_resource(views.Files, '/api/files')


def init_db(db, drop_all=False):
    """
    Initialize the database
    """
    print("Initializing DB {}".format(db))
    db.init_app(flask_app)
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
    parser.add_argument('--dropall', action="store_true", required=False,
                        help='drop tables in database before starting')
    parser.add_argument('--initonly', action="store_true", required=False,
                        help='just init database and do nothing else')
    args = parser.parse_args()

    init_db(db, drop_all=args.dropall)
    if args.initonly:
        sys.exit(0)

    flask_app.run(debug=True)
