class UndefinedException(Exception):
    pass


class CreateUserError(UndefinedException):
    pass


class UserAlreadyExistsError(UndefinedException):
    pass


class UserNotFoundError(UndefinedException):
    pass
