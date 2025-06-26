# echospace/server/app/routes/mood_routes.py

from flask import Blueprint, jsonify
from ..models import Mood

mood_bp = Blueprint("mood_bp", __name__)

@mood_bp.route("/moods", methods=["GET"])
def get_moods():
    moods = Mood.query.all()
    return jsonify([mood.to_dict() for mood in moods])
