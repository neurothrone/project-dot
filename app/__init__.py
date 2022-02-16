from datetime import datetime

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
import jinja_partials

from .config import configure, ConfigType
from .cli import register_cli_commands
from .shell import setup_shell_context_processor

login_manager = LoginManager()
mail = Mail()
moment = Moment()


def create_app(config_type: ConfigType | None = None) -> Flask:
    app = Flask(__name__)

    configure(app, config_type)
    initialize_extensions(app)
    register_blueprints(app)
    register_injections(app)
    register_template_funcs(app)
    register_jinja_filters(app)
    register_cli_commands(app)
    setup_shell_context_processor(app)

    return app


def initialize_extensions(app: Flask) -> None:
    jinja_partials.register_extensions(app)
    mail.init_app(app)
    moment.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # endpoint for login page
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    from .schemas.user import AnonymousUser
    login_manager.anonymous_user = AnonymousUser

    from .controllers.user import UserController
    from .schemas.complex import UserOutWithProfile

    @login_manager.user_loader
    def load_user(user_id: str) -> UserOutWithProfile | None:
        return UserController.get_model_by_username(user_id)

    # if app.config.get("SSL_REDIRECT", False):
    #     from flask_sslify import SSLify
    #     sslify = SSLify(app)


def register_blueprints(app: Flask) -> None:
    from .blueprints.admin import bp_admin
    app.register_blueprint(bp_admin, url_prefix="/admin")

    from .blueprints.api import bp_api
    app.register_blueprint(bp_api, url_prefix="/api")

    from .blueprints.auth import bp_auth
    app.register_blueprint(bp_auth, url_prefix="/auth")

    from .blueprints.open import bp_open
    app.register_blueprint(bp_open)

    from .blueprints.user import bp_user
    app.register_blueprint(bp_user)


def register_injections(app: Flask) -> None:
    @app.context_processor
    def inject_utility():
        return dict(now=datetime.utcnow())


def register_template_funcs(app: Flask) -> None:
    helpers = {
        "isinstance": isinstance,
        "len": len,
        "str": str,
        "type": type
    }

    app.jinja_env.auto_reload = True
    app.jinja_env.cache = {}
    app.jinja_env.globals.update(**helpers)


def register_jinja_filters(app: Flask) -> None:
    from .shared.filters.dt import date_format, time_format, datetime_format, time_of_day_message
    from .shared.filters.flash import flash_category_color

    app.jinja_env.filters["date"] = date_format
    app.jinja_env.filters["time"] = time_format
    app.jinja_env.filters["datetime"] = datetime_format
    app.jinja_env.filters["day"] = time_of_day_message
    app.jinja_env.filters["flash"] = flash_category_color
