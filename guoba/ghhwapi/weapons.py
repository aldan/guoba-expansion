from flask import Blueprint, request, jsonify
import ghhw

weapons = Blueprint('weapons', __name__, url_prefix='/weapons')


@weapons.route('/', methods=['GET'])
def get_weapons():
    return jsonify(ghhw.get_weapons(**request.args))


@weapons.route('/<string:weapon_id>', methods=['GET'])
def get_weapon(weapon_id):
    return jsonify(ghhw.get_weapons(id=weapon_id))
