from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from .config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)  # <-- fixed

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Setup CORS
    CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5173"}}, supports_credentials=True)

    # Register Blueprints (use consistent URL prefixes!)
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api")


    from .routes.post_routes import post_bp
    app.register_blueprint(post_bp, url_prefix="/api")

    from .routes.comment_routes import comment_bp
    app.register_blueprint(comment_bp, url_prefix="/api")

    from .routes.mood_routes import mood_bp
    app.register_blueprint(mood_bp, url_prefix="/api")

    from .routes.reaction_routes import reaction_bp
    app.register_blueprint(reaction_bp, url_prefix="/api")

    return app