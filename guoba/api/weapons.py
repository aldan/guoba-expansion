from flask import Blueprint, jsonify
from guoba.models import Weapon

weapons = Blueprint('weapons', __name__, url_prefix='/weapons')


@weapons.route('/', methods=['GET'])
def get_weapons():
    db_weapons = Weapon.query.all()
    return jsonify([weapon.serialize for weapon in db_weapons])
