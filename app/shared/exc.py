class UserRepositoryError(Exception):
    def __init__(self, message: str):
        raise Exception(message)


class UserDoesNotExist(UserRepositoryError):
    pass


class UsernameAlreadyTakenError(UserRepositoryError):
    pass


class EmailAlreadyTakenError(UserRepositoryError):
    pass
