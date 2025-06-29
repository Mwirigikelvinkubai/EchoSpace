from . import db
from datetime import datetime
from passlib.hash import pbkdf2_sha256


# ------------------ USER ------------------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    posts = db.relationship('Post', back_populates='user', lazy=True)
    comments = db.relationship('Comment', back_populates='user', lazy=True)
    moods = db.relationship('Mood', back_populates='user', lazy=True)
    reactions = db.relationship('Reaction', back_populates='user', lazy=True)

    def set_password(self, pw):
        self.password_hash = pbkdf2_sha256.hash(pw)

    def check_password(self, pw):
        return pbkdf2_sha256.verify(pw, self.password_hash)
 
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood_id = db.Column(db.Integer, db.ForeignKey('moods.id'), nullable=True)

    user = db.relationship('User', back_populates='posts')
    mood = db.relationship('Mood', back_populates='posts')  # ✅ Needed for proper join
    comments = db.relationship('Comment', back_populates='post', lazy=True, cascade="all, delete-orphan")
    reactions = db.relationship('Reaction', back_populates='post', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "is_anonymous": self.is_anonymous,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "mood_id": self.mood_id,
            "username": self.user.username if not self.is_anonymous else "Anonymous"
        }


# ------------------ COMMENT ------------------
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'user': self.user.username,
            'post_id': self.post_id
        }


# ------------------ MOOD ------------------
class Mood(db.Model):
    __tablename__ = 'moods'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='moods')
    posts = db.relationship('Post', back_populates='mood', lazy=True)  # ✅ Matches Post.mood

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "user_id": self.user_id
        }


# ------------------ REACTION ------------------
class Reaction(db.Model):
    __tablename__ = 'reactions'

    id = db.Column(db.Integer, primary_key=True)
    emoji = db.Column(db.String(10), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship('User', back_populates='reactions')
    post = db.relationship('Post', back_populates='reactions')
