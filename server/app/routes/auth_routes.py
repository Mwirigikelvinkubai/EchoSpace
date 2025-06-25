from flask import Blueprint, jsonify

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/ping")
def ping():
    return jsonify({"message": "Auth routes working!"})
