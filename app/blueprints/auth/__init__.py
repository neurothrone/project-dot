from flask import Blueprint

bp_auth = Blueprint(name="auth", import_name=__name__)

from app.blueprints.auth import routes
