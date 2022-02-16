from .. import BaseTestCase
from app.controllers.project import ProjectController
from shared.generators.project import ProjectGenerator


class ProjectModelTestCase(BaseTestCase):
    def test_create(self):
        project = ProjectGenerator.generate()
        self.assertIsNotNone(project)

    def test_find_all(self):
        len_projects = 3
        ProjectGenerator.generate_many(amount=len_projects)
        projects = ProjectController.get_all()
        self.assertIsInstance(projects, list)
        self.assertTrue(len(projects) == len_projects)
