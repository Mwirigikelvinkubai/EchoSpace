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
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

   
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    # Register Blueprints
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from .routes.post_routes import post_bp
    app.register_blueprint(post_bp)

    from .routes.comment_routes import comment_bp
    app.register_blueprint(comment_bp)

    from .routes.mood_routes import mood_bp
    app.register_blueprint(mood_bp, url_prefix="/moods")

    from .routes.reaction_routes import reaction_bp
    app.register_blueprint(reaction_bp, url_prefix="/api")

    return app
