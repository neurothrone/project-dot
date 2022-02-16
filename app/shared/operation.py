# TODO: namedtuple seems better?
# TODO: use these on view models? Keep Controllers clean

class Operation:
    def __init__(self,
                 detail: str = "",
                 status_code: int = 0,
                 was_successful: bool = False):
        self.detail = detail
        self.status_code = status_code
        self.was_successful = was_successful

    def to_response(self) -> dict:
        pass
