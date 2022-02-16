from app.controllers.profile import ProfileController
from app.schemas.profile import ProfileIn
from shared.data.fake import FakeData
from shared.generators import BaseGenerator


class ProfileGenerator(BaseGenerator):
    controller = ProfileController
    model_in = ProfileIn

    @classmethod
    def random_data(cls, full_name: str = None) -> dict:
        name, surname = FakeData.full_name().split(" ") if not full_name else full_name.split(" ")
        return {
            "name": name,
            "surname": surname,
            "city": FakeData.city(),
            "headline": FakeData.text(sentences=1),
            "bio": FakeData.text(sentences=3),
            "social_website": FakeData.url()
        }
