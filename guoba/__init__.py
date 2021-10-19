# Application Factory

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')  # todo remove
    CORS(app, origins=["http://localhost:3000"])        # todo remove

    db.init_app(app)
    Migrate(app, db)
    with app.app_context():
        db.create_all()
        db.session.commit()

    from .api import api
    from .ghhwapi import ghhwapi
    from .dbtools import dbtools

    app.register_blueprint(api)
    app.register_blueprint(ghhwapi)
    app.register_blueprint(dbtools)

    return app
