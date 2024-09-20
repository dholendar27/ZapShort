from flask import Flask
from .extensions import db, migrate
from .routes import main
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(config_file='config.py'):
    app = Flask(__name__)
    CORS(app)
    app.config.from_pyfile(config_file)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main)

    jwt = JWTManager(app)

    return app
