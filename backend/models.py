"""
Models for the item service
"""
# native imports
import json
from datetime import datetime

# third party imports
import bcrypt

from backend import db


class JsonEncodedDict(db.TypeDecorator):
    """
    Enables JSON storage by encoding and decoding on the fly.
    """
    impl = db.Text

    def process_bind_param(self, value, dialect):
        """
        Create string from JSON dict
        """
        if value is None:
            return '{}'
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        """
        Create a JSON dict from string
        """
        if value is None:
            return {}
        return json.loads(value)


class User(db.Model):
    """
    A user can log in to services
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), unique=False, nullable=False)
    items = db.relationship('Item', backref='user', lazy=True)
    files = db.relationship('File', backref='user', lazy=True)

    def __repr__(self):
        """
        String representation for a user
        """
        return '<User {id} email={email}>'.format(id=self.id, email=self.email)

    @staticmethod
    def generate_hash(plaintext_password):
        """
        Generates and returns a salted password hash
        """
        return bcrypt.hashpw(plaintext_password, bcrypt.gensalt())


class Item(db.Model):
    """
    A item contains a list of ingredients and a list of steps
    """
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    field1 = db.Column(db.String(100), unique=False, nullable=False)
    jsonfield1 = db.Column(JsonEncodedDict, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def as_json(self, user_id=None):
        """
        JSON representation of this model
        """
        payload = {
            "id": self.id,
            # "user_id": self.user.id, # this is sensitive, let's not reveal it
            "field1": self.field1,
            "jsonfield1": self.jsonfield1,
            "created_on": self.created_on.strftime("%m/%d/%Y %H:%M:%S"),
            "owner": False
        }
        # if the user requesting this item
        # is specified and they own it, let the frontend know
        if user_id is not None and user_id == self.user_id:
            payload['owner'] = True

        return payload


class File(db.Model):
    """
    A file is uploaded by a user and has a unique name
    """
    __tablename__ = "file"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(500), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class RevokedTokenModel(db.Model):
    """
    Store revoked tokens
    """
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        """
        Add a token to the revoked tokens list
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """
        Check if a token is blacklisted
        """
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
