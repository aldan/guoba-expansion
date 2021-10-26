from flask import Blueprint
from .characters import characters
from .collections import collections
from .weapons import weapons

api = Blueprint('api', __name__, url_prefix='/api')

api.register_blueprint(characters)
api.register_blueprint(weapons)
api.register_blueprint(collections)
