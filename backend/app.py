#!/usr/bin/env python3
"""
Item API backend. This is the main entry point for the app.
"""

# native imports
import base64
import argparse

# flask imports
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# my imports, some from __init__
from backend import api, app, db, auth
from backend.models import Item, User


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
        if request.args.get('id') is not None:
            return [x.as_json() for x in Item.query.filter(Item.name.contains(request.args.get('id')))]
        return [x.as_json() for x in Item.query.all()], 200

    @jwt_required
    def put(self):
        """
        Update an existing item
        """
        if 'field1' not in request.json:
            return {'error': 'missing field1'}, 400
        if 'jsonfield1' not in request.json:
            return {'error': 'missing jsonfield1'}, 400
        if not request.json['field1']:
            return {'error': 'field1 must not be 0 length'}, 400
        if not request.json['jsonfield1']:
            return {'error': 'jsonfield1 must not be 0 length'}, 400
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
        if 'field1' not in request.json:
            return {'error': 'missing field1'}, 400
        if 'jsonfield1' not in request.json:
            return {'error': 'missing jsonfield1'}, 400
        if not request.json['field1']:
            return {'error': 'field1 must not be 0 length'}, 400
        if not request.json['jsonfield1']:
            return {'error': 'jsonfield1 must not be 0 length'}, 400
        user = User.query.filter_by(email=get_jwt_identity()).first()
        item = Item(field1=request.json['field1'],
                    jsonfield1=request.json['jsonfield1'],
                    user=user)
        db.session.add(item)
        db.session.commit()
        return [x.as_json() for x in Item.query.all()], 200


# endpoints here
api.add_resource(Items, '/api/items')


def init_db(test_data=False, drop_all=False):
    """
    Initialize the database
    """
    print("Initializing DB")
    db.init_app(app)
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
    args = parser.parse_args()

    init_db(test_data=args.testdata, drop_all=args.dropall)
    app.run(debug=True)
