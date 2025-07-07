from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from .db import db

class Mood(db.Model, SerializerMixin):
    __tablename__ = 'moods'

    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50), nullable=False)
    note = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='moods')

    serialize_rules = ('-user.moods',)

    @validates('mood')
    def validate_mood(self, key, value):
        assert value.strip(), "Mood is required"
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "mood": self.mood,
            "note": self.note,
            "timestamp": self.timestamp.isoformat()
        }

    def __repr__(self):
        return f"<Mood {self.mood}>"
