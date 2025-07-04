from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from .db import db

class Reaction(db.Model, SerializerMixin):
    __tablename__ = 'reactions'

    id = db.Column(db.Integer, primary_key=True)
    emoji = db.Column(db.String(10), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship('User', back_populates='reactions')
    post = db.relationship('Post', back_populates='reactions')

    serialize_rules = ('-user.reactions', '-post.reactions')

    @validates('emoji')
    def validate_emoji(self, key, emoji):
        assert emoji.strip() != '', "Emoji cannot be empty"
        return emoji

    def __repr__(self):
        return f"<Reaction '{self.emoji}' on Post {self.post_id}>"