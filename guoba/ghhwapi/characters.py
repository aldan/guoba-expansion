from flask import Blueprint, request, jsonify
import ghhw

characters = Blueprint('characters', __name__, url_prefix='/characters')


@characters.route('/', methods=['GET'])
def get_characters():
    return jsonify(ghhw.get_characters(**request.args))


@characters.route('/<string:character_id>', methods=['GET'])
def get_character(character_id):
    return jsonify(ghhw.get_characters(id=character_id))
