# Application Factory

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')  # todo remove
    CORS(app, origins=["http://localhost:3000"])        # todo remove

    db.init_app(app)
    Migrate(app, db)
    with app.app_context():
        db.create_all()

    from .api import api
    from .ghhwapi import ghhwapi
    from .syncdb import syncdb

    app.register_blueprint(api)
    app.register_blueprint(ghhwapi)
    app.register_blueprint(syncdb)

    return app
