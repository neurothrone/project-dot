from app.controllers.user import UserController, UserIn, UserOutAll
from shared.data.fake import FakeData
from shared.generators import BaseGenerator


class UserGenerator(BaseGenerator):
    controller = UserController
    model_in = UserIn

    @classmethod
    def generate_many(cls,
                      amount: int,
                      unique: bool = True
                      ) -> list[UserOutAll]:
        if not unique:
            return super().generate_many(amount=amount)

        full_names = FakeData.generate_full_names(amount=amount, unique=unique)
        users_data = []
        for index in range(amount):
            name, surname = full_names[index].lower().split(" ")
            users_data.append({
                "email": f"{name}.{surname}@example.com",
                "username": f"{name}{surname}",
                "password": FakeData.password()
            })

        return [UserController.create(UserIn(**user_data)) for user_data in users_data]

    @classmethod
    def generate_many_with_profiles(cls,
                                    amount: int,
                                    unique: bool = True
                                    ) -> list[UserOutAll]:
        full_names = FakeData.generate_full_names(amount=amount, unique=unique)
        users = []

        for index in range(amount):
            name, surname = full_names[index].lower().split(" ")
            user = UserController.create_with_profile(UserIn(**{
                "username": f"{name}{surname}",
                "email": f"{name}.{surname}@example.com",
                "password": FakeData.password()
            }))

            # TODO: use random_data() from ProfileGenerator to populate profiles

            users.append(user)

        return users

    @classmethod
    def random_data(cls) -> dict:
        name, surname = FakeData.full_name().lower().split(" ")
        return {
            "username": f"{name}{surname}",
            "email": f"{name}.{surname}@example.com",
            "password": FakeData.password()
        }
