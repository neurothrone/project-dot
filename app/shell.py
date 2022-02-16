from flask import Flask


def setup_shell_context_processor(_app: Flask) -> None:
    @_app.shell_context_processor
    def make_shell_context():
        from app.data.db import db
        from app.data.models.profile import ProfileDB
        from app.data.models.project import ProjectDB
        from app.data.models.user import UserDB

        return dict(db=db,
                    Profile=ProfileDB,
                    Project=ProjectDB,
                    User=UserDB)
