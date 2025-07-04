from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from .db import db

class Mood(db.Model, SerializerMixin):
    __tablename__ = 'moods'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='moods')
    posts = db.relationship('Post', back_populates='mood', cascade='all, delete-orphan')

    serialize_rules = ('-user.moods', '-posts.mood')

    @validates('label')
    def validate_label(self, key, label):
        assert label.strip() != '', "Mood label is required"
        return label

    def __repr__(self):
        return f"<Mood '{self.label}'>"