import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'app.db')

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key")  # safer
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False  
    JWT_COOKIE_CSRF_PROTECT = False 
