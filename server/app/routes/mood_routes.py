# echospace/server/app/routes/mood_routes.py

from flask import Blueprint, jsonify
from ..models import Mood
from flask_jwt_extended import(JWTManager,create_access_token,jwt_required,get_jwt_identity,
set_access_cookies,set_refresh_cookies,unset_jwt_cookies)

mood_bp = Blueprint("mood_bp", __name__)

@mood_bp.route("/moods", methods=["GET"])
def get_moods():
    moods = Mood.query.all()
    return jsonify([mood.serialize() for mood in moods])

