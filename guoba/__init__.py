# Application Factory

import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid


db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    Migrate(app, db)
    from .models import Collection

    with app.app_context():
        db.create_all()

    from . import collection
    from .api import api
    from .ghhwapi import ghhwapi
    from .syncdb import syncdb

    app.register_blueprint(api)
    app.register_blueprint(ghhwapi)
    app.register_blueprint(collection.bp)
    app.register_blueprint(syncdb)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            request_type = request.form.get('type')
            db_entry = Collection()
            db.session.add(db_entry)
            db.session.commit()

            return redirect(url_for('collection.collection', collection_id=db_entry.id))
        return 'index'

    return app
