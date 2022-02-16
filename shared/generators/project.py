from app.controllers.project import ProjectController, ProjectIn
from shared.data.fake import FakeData
from shared.generators import BaseGenerator


class ProjectGenerator(BaseGenerator):
    controller = ProjectController
    model_in = ProjectIn

    @classmethod
    def random_data(cls) -> dict:
        title = FakeData.text(sentences=1)
        if len(title) > 64:
            title = title[:63]
        return {
            "title": title,
            "description": FakeData.text(sentences=3),
            "demo_link": FakeData.url(),
            "source_link": FakeData.url(),
        }
