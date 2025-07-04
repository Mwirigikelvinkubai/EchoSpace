from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .db import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(200), nullable=False)

    posts = db.relationship('Post', back_populates='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')
    moods = db.relationship('Mood', back_populates='user', cascade='all, delete-orphan')
    reactions = db.relationship('Reaction', back_populates='user', cascade='all, delete-orphan')

    serialize_rules = ('-password_hash', '-comments.user', '-posts.user', '-reactions.user')

    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Email must contain '@'"
        return email

    @validates('username')
    def validate_username(self, key, username):
        assert len(username) >= 3, "Username must be at least 3 characters"
        return username

    def __repr__(self):
        return f"<User {self.username}>"
