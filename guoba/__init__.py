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
        from .models import Character, Weapon, Collection
        db.create_all()
        db.session.commit()

    @app.errorhandler(401)
    def unauthorized(e):
        return {
                   'success': False,
                   'error': str(e),
               }, 401

    @app.errorhandler(404)
    def not_found(e):
        return {
                   'success': False,
                   'error': str(e),
               }, 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return {
                   'success': False,
                   'error': str(e),
               }, 405

    @app.errorhandler(422)
    def unprocessable_entity(e):
        return {
            'success': False,
            'error': str(e),
        }, 422

    @app.errorhandler(500)
    def internal_server_error(e):
        return {
                   'success': False,
                   'error': str(e),
               }, 500

    from .api import api
    from .ghhwapi import ghhwapi
    from .dbtools import dbtools

    app.register_blueprint(api)
    app.register_blueprint(ghhwapi)
    app.register_blueprint(dbtools)

    return app
