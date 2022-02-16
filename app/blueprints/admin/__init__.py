from flask import Blueprint

bp_admin = Blueprint(name="admin", import_name=__name__)

from app.blueprints.admin import routes
