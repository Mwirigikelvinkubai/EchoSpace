from flask import Blueprint, request, jsonify
from app.models import db, Post, User
from flask_jwt_extended import jwt_required, get_jwt_identity

post_bp = Blueprint("post_bp", __name__)

# Create a new post
@post_bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()

    post = Post(
        content=data.get("content"),
        is_anonymous=data.get("is_anonymous", True),
        user_id=user_id
    )
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

# Get all posts (feed)
@post_bp.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

# Get current user's posts
@post_bp.route("/posts/mine", methods=["GET"])
@jwt_required()
def get_my_posts():
    user_id = get_jwt_identity()
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.timestamp.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

# Delete a post
@post_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get(post_id)
    if not post or post.user_id != user_id:
        return jsonify({"error": "Post not found or not authorized"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"}), 200
