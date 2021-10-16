from flask import Blueprint
from .characters import characters
from .weapons import weapons

api = Blueprint('api', __name__, url_prefix='/api')
api.register_blueprint(characters)
api.register_blueprint(weapons)
