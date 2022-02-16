from .. import BaseTestCase
from app.controllers.profile import ProfileController
from app.controllers.project import ProjectController
from shared.generators.profile import ProfileGenerator
from shared.generators.project import ProjectGenerator


class ProfileModelTestCase(BaseTestCase):
    def test_create(self):
        profile = ProfileGenerator.generate()
        self.assertIsNotNone(profile)

    def test_find_all(self):
        len_profiles = 3
        ProfileGenerator.generate_many(amount=len_profiles)
        profiles = ProfileController.get_all()
        self.assertIsInstance(profiles, list)
        self.assertTrue(len(profiles) == len_profiles)

    def test_profile_relationship_with_projects(self):
        profile = ProfileGenerator.generate()

        # create projects
        len_projects = 3
        projects = ProjectGenerator.generate_many(amount=len_projects)
        self.assertTrue(len(projects) == len_projects)

        # add projects to profile
        for project in projects:
            ProfileController.add_project(project, profile)

        for project in profile.projects:
            self.assertIsNotNone(project)

        self.assertIsInstance(profile.projects, list)
        self.assertTrue(len(profile.projects) == len_projects)

        # remove projects
        for _ in range(len_projects):
            self.assertTrue(len(profile.projects) == len_projects)
            ProfileController.remove_project(profile.projects[len_projects - 1], profile)
            len_projects -= 1

        self.assertEqual(profile.projects, [])

        # check projects
        projects = ProjectController.get_all()
        for project in projects:
            self.assertIsNone(project.profile_id)

    def test_delete_profile_cascade_to_projects(self):
        profile = ProfileGenerator.generate()

        # create projects
        len_projects = 3
        projects = ProjectGenerator.generate_many(amount=len_projects)
        self.assertTrue(len(projects) == len_projects)

        # add projects
        for project in projects:
            ProfileController.add_project(project, profile)
        self.assertTrue(len(profile.projects) == len_projects)

        # delete profile
        profile.delete()

        # check projects deleted from cascade
        projects = ProjectController.get_all()
        self.assertEqual(projects, [])

# TODO: test avatar hash changed upon changing email
