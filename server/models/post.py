from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from .db import db

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood_id = db.Column(db.Integer, db.ForeignKey('moods.id'))

    user = db.relationship('User', back_populates='posts')
    mood = db.relationship('Mood', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    reactions = db.relationship('Reaction', back_populates='post', cascade='all, delete-orphan')

    serialize_rules = ('-user.posts', '-comments.post', '-reactions.post')

    @validates('content')
    def validate_content(self, key, content):
        assert content.strip() != '', "Post content cannot be empty"
        return content

    def __repr__(self):
        return f"<Post {self.id} by User {self.user_id}>"