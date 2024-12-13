class UserCannotBeCreatedError(Exception):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


class UserNotFoundError(Exception):
    pass
