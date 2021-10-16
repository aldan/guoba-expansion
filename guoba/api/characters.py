from flask import Blueprint, jsonify
from guoba.models import Character

characters = Blueprint('characters', __name__, url_prefix='/characters')


@characters.route('/', methods=['GET'])
def get_characters():
    db_characters = Character.query.all()
    return jsonify([character.serialize for character in db_characters])
