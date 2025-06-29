from flask import Blueprint, request, jsonify, current_app
from .. import db, bcrypt
from ..models import User
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies
)
from datetime import timedelta
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create blueprint
auth_bp = Blueprint("auth_bp", __name__)

# JWT config should go into app, not blueprint
# You will do this in create_app() when you register JWT

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data.get("email") or not data.get("password") or not data.get("username"):
        return jsonify(message="Missing required fields"), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(email=data["email"], username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    resp = jsonify(message="Registered successfully")
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify(message='Missing email or password'), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify(message='Invalid credentials'), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    resp = jsonify(
        message="Login successful",
        user=user.to_dict() if hasattr(user, "to_dict") else {"id": user.id, "email": user.email, "username": user.username}
    )
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    resp = jsonify(message="Token refreshed")
    set_access_cookies(resp, access_token)
    return resp, 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    resp = jsonify(message="Logged out")
    unset_jwt_cookies(resp)
    return resp, 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404
    return jsonify(user.to_dict() if hasattr(user, "to_dict") else {"id": user.id, "email": user.email, "username": user.username}), 200