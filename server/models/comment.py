from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from .db import db

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

    serialize_rules = ('-user.comments', '-post.comments')

    @validates('content')
    def validate_content(self, key, content):
        assert content.strip() != '', "Comment cannot be empty"
        return content

    def __repr__(self):
        return f"<Comment {self.id} on Post {self.post_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "user": self.user.username if self.user else "Anonymous",
            "post_id": self.post_id
        }
