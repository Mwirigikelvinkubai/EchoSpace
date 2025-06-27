from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    moods = db.relationship('Mood', backref='user', lazy=True)
    reactions = db.relationship('Reaction', backref='user', lazy=True)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "is_anonymous": self.is_anonymous,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "username": self.user.username if not self.is_anonymous else "Anonymous"
        }

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'user': self.user.username,
            'post_id': self.post_id
        }

class Mood(db.Model):
    __tablename__ = 'moods'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False, unique=True)

    posts = db.relationship('Post', backref='mood', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'label': self.label
        }

class Reaction(db.Model):
    __tablename__ = 'reactions'

    id = db.Column(db.Integer, primary_key=True)
    emoji = db.Column(db.String(10), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
