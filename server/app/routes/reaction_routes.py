# echospace/server/app/routes/reaction_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import(JWTManager,create_access_token,jwt_required,get_jwt_identity,
set_access_cookies,set_refresh_cookies,unset_jwt_cookies)
from ..models import db, Reaction

reaction_bp = Blueprint("reaction_bp", __name__)

@reaction_bp.route("/reactions", methods=["POST"])
@jwt_required()
def add_reaction():
    data = request.json
    user_id = get_jwt_identity()
    new_reaction = Reaction(
        emoji=data["emoji"],
        user_id=user_id,
        post_id=data["post_id"]
    )
    db.session.add(new_reaction)
    db.session.commit()
    return jsonify(new_reaction.to_dict()), 201

@reaction_bp.route("/posts/<int:post_id>/reactions", methods=["GET"])
def get_reactions(post_id):
    reactions = Reaction.query.filter_by(post_id=post_id).all()
    return jsonify([r.to_dict() for r in reactions])
