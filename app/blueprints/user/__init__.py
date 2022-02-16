from flask import Blueprint

bp_user = Blueprint(name="user", import_name=__name__)

from . import routes
