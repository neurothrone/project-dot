from flask import Blueprint

bp_api = Blueprint(name="api",
                   import_name=__name__)

from . import endpoints
