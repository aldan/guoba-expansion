# Collection blueprint
import uuid

from flask import Blueprint, request
from .models import Collection
# from . import db
bp = Blueprint('collection', __name__, url_prefix='/collection')


@bp.route('/<uuid:collection_id>', methods=['GET', 'POST'])
def collection(collection_id):
    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{collection_id}")
    if request.method == 'POST':
        return "Turn"
    db_entry = Collection.query.get(collection_id)
    return str(db_entry.id)
