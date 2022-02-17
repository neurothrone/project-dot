from os import getenv

from flask import Flask


def register_cli_commands(_app: Flask) -> None:
    @_app.cli.command()
    def test():
        """Runs all the unit tests of this project.

        Open a terminal and navigate to this project's root
        directory and type 'flask test' to run all tests.
        """

        import unittest
        tests = unittest.TestLoader().discover("tests")
        unittest.TextTestRunner(verbosity=2).run(tests)

    @_app.cli.command("generate-data")
    def generate_data():
        from app.controllers.profile import ProfileController
        from app.schemas.complex import ProfileOutWithProjects
        from shared.generators.user import UserGenerator
        from shared.generators.project import ProjectGenerator

        projects: list[ProfileOutWithProjects] = ProjectGenerator.generate_many(amount=25)
        users = UserGenerator.generate_many_with_profiles(amount=25, unique=True)

        for project, user in zip(projects, users):
            try:
                ProfileController.add_existing_project_to_user(project.id, user.id)
            except ValueError:
                pass

    @_app.cli.command("setup-admin")
    def setup_admin():
        from app.controllers.profile import ProfileController
        from app.controllers.user import UserController
        from app.shared.access import AccessLevel
        from app.schemas.user import UserIn
        from app.schemas.complex import ProfileOutWithProjects
        from shared.generators.project import ProjectGenerator

        from dotenv import load_dotenv
        load_dotenv()

        user = UserController.create_with_profile(UserIn(
            username=getenv("ADMIN_USER"),
            email=getenv("ADMIN_EMAIL"),
            password=getenv("ADMIN_PASS"),
            is_confirmed=True,
            access_level=AccessLevel.ADMIN))
        projects: list[ProfileOutWithProjects] = ProjectGenerator.generate_many(amount=5)
        for project in projects:
            ProfileController.add_existing_project_to_user(project.id, user.id)
