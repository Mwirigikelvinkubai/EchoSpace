from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, set_access_cookies, unset_jwt_cookies
)
from datetime import timedelta
from sqlalchemy.exc import IntegrityError

from config import Config
from models import db, User, Post, Comment, Mood

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

# JWT config
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False  # Use True in production
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token"}), 422

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "Authorization header missing"}), 401

# DB and CORS setup
db.init_app(app)
migrate = Migrate(app, db)
CORS(app, supports_credentials=True)
api = Api(app)


@app.route('/')
def home():
    return '<h1>EchoSpace is running</h1>'


# AUTH ROUTES 

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    user = User(username=username, email=email)
    user.password_hash = password

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already taken"}), 409
    except AssertionError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "User created successfully"}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        resp = jsonify({"login": True})
        set_access_cookies(resp, access_token)
        return resp, 200

    return jsonify({"login": False}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    response = jsonify({"logout": True})
    unset_jwt_cookies(response)
    return response, 200


@app.route('/api/refresh', methods=['POST'])
@jwt_required()
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    response = jsonify({"refresh": True})
    set_access_cookies(response, access_token)
    return response, 200


@app.route('/api/me', methods=['GET'])
@jwt_required()
def get_me():
    user = User.query.filter_by(username=get_jwt_identity()).first()
    return jsonify(user.to_dict()), 200


#  COMMENT ROUTES 

@app.route('/api/comments', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    content = data.get("content")
    post_id = data.get("post_id")

    if not content or not post_id:
        return jsonify({"error": "Missing content or post_id"}), 400

    user = User.query.filter_by(username=get_jwt_identity()).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    comment = Comment(content=content, user=user, post=post)
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201


@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_comments_for_post(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return jsonify([comment.to_dict() for comment in comments]), 200


@app.route('/api/me/comments', methods=['GET'])
@jwt_required()
def get_my_comments():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    comments = []
    for c in user.comments:
        c_data = c.to_dict()
        c_data["post_content"] = c.post.content if c.post else "Deleted post"
        comments.append(c_data)

    return jsonify(comments), 200
    
@app.route('/api/moods', methods=['POST'])
@jwt_required()
def create_mood():
    data = request.get_json()
    mood = data.get("mood")
    note = data.get("note", "")

    if not mood:
        return jsonify({"error": "Mood is required"}), 400

    user = User.query.filter_by(username=get_jwt_identity()).first()
    entry = Mood(mood=mood, note=note, user=user)
    db.session.add(entry)
    db.session.commit()

    return jsonify(entry.to_dict()), 201

@app.route('/api/me/moods', methods=['GET'])
@jwt_required()
def get_my_moods():
    user = User.query.filter_by(username=get_jwt_identity()).first()
    moods = [m.to_dict() for m in user.moods]
    return jsonify(moods), 200





if __name__ == '__main__':
    app.run(port=5555, debug=True)
