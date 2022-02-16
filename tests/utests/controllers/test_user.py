from .. import BaseTestCase
from app.controllers.profile import ProfileController
from app.controllers.user import UserController
from shared.generators.profile import ProfileGenerator
from shared.generators.user import UserGenerator


class UserModelTestCase(BaseTestCase):
    def test_create(self):
        user = UserGenerator.generate()
        self.assertIsNotNone(user)

    def test_user_relationship_with_profile(self):
        profile = ProfileGenerator.generate()
        user = UserGenerator.generate()

        UserController.add_profile(profile, user)

        self.assertIsNotNone(profile.account)
        self.assertIsNotNone(user.profile)
        self.assertTrue(user.profile.user_id == profile.user_id)
        self.assertTrue(user.profile.id == profile.id)

        UserController.remove_profile(user)

        self.assertIsNone(profile.user_id)
        self.assertIsNone(profile.account)
        self.assertIsNone(user.profile)

    def test_delete_user_cascade_to_profile(self):
        profile = ProfileGenerator.generate()
        user = UserGenerator.generate()

        UserController.add_profile(profile, user)

        self.assertIsNotNone(user.profile)

        user.delete()
        profile = ProfileController.get_by_name(profile.name)
        self.assertIsNone(profile)

    def test_search_for_usernames(self):
        UserGenerator.generate_many(amount=50, unique=True)
        search_for = "a"
        users = UserController.get_all_ilike_username(search_for)
        self.assertIsNotNone(users)

    def test_connect_profiles_to_existing_users(self):
        UserGenerator.generate_many(amount=10, unique=True)
        UserGenerator.add_profiles_to_existing_users()

        users = UserController.get_all()
        for user in users:
            self.assertIsNotNone(user.profile)

    def test_add_profile_to_confirmed_user(self):
        user = UserGenerator.generate()
        UserController.add_profile_to_confirmed_user(user)
        self.assertIsNotNone(user.profile)
        self.assertIsNotNone(user.profile.avatar_hash)

    def test_delete_account(self):
        # Create User, Profile and link them
        user = UserGenerator.generate()
        UserController.add_profile_to_confirmed_user(user)
        user.profile.name = "jane"

        self.assertIsNotNone(user.profile)
        self.assertIsNotNone(user.profile.name)

        # Store what to search for before deletion of user
        username = user.username
        name = user.profile.name
        user.delete()

        # Confirm that deletion of User also deletes linked Profile
        found_user = UserController.get_by_username(username)
        found_profile = ProfileController.get_by_name(name)

        self.assertIsNone(found_user)
        self.assertIsNone(found_profile)
