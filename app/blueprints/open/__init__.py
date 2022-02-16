from flask import Blueprint

bp_open = Blueprint(name="open", import_name=__name__)

from . import routes
