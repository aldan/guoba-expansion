from flask import Blueprint
from .characters import characters
from .weapons import weapons
ghhwapi = Blueprint('ghhwapi', __name__, url_prefix='/ghhwapi')

ghhwapi.register_blueprint(characters)
ghhwapi.register_blueprint(weapons)
