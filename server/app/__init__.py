from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager  # ✅ Add this

from .config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()  # ✅ Add this

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)  # ✅ Add this
    CORS(app)

    # Auth routes
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Post routes
    from .routes.post_routes import post_bp
    app.register_blueprint(post_bp)  

    # Comments routes
    from .routes.comment_routes import comment_bp
    app.register_blueprint(comment_bp)

    # Mood
    from .routes.mood_routes import mood_bp
    app.register_blueprint(mood_bp, url_prefix="/moods")

    # Reaction
    from .routes.reaction_routes import reaction_bp
    app.register_blueprint(reaction_bp, url_prefix="/api")

    return app
