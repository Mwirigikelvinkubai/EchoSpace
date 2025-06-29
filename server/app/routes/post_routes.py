from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Post
from flask_jwt_extended import(JWTManager,create_access_token,jwt_required,get_jwt_identity,
set_access_cookies,set_refresh_cookies,unset_jwt_cookies)

post_bp = Blueprint("post_bp", __name__)

# Create a new post
@post_bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json()
    content = data.get("content")
    is_anonymous = data.get("is_anonymous", False)
    user_id = get_jwt_identity()

    if not content:
        return jsonify({"error": "Content is required"}), 422

    new_post = Post(
        content=content,
        is_anonymous=is_anonymous,
        user_id=user_id
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 201


# Get all posts (feed)
@post_bp.route("/posts", methods=["GET"])
def get_posts():
    try:
        posts = Post.query.order_by(Post.timestamp.desc()).all()
        return jsonify([post.to_dict() for post in posts]), 200
    except Exception as e:
      
        return jsonify({"error": "Internal server error"}), 500

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

    if not post:
        return jsonify({"error": "Post not found"}), 404

    if post.user_id != user_id:
        return jsonify({"error": "Not authorized to delete this post"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"}), 200
