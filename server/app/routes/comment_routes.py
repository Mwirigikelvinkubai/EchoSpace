from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Comment, User, Post

comment_bp = Blueprint('comment_bp', __name__)

@comment_bp.route('/comments', methods=['POST'])
@jwt_required()
def add_comment():
    data = request.get_json()
    user_id = get_jwt_identity()
    content = data.get('content')
    post_id = data.get('post_id')

    if not content or not post_id:
        return jsonify({"error": "Missing content or post_id"}), 400

    comment = Comment(content=content, user_id=user_id, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.serialize()), 201

@comment_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.asc()).all()
    return jsonify([c.serialize() for c in comments]), 200
