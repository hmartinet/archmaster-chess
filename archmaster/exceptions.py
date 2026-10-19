

class UserException(Exception):
    def __init__(self, user_message, *args):
        super().__init__(user_message, *args)
        self.user_message = user_message


class MigrationUserException(UserException):
    pass


class ImportUserException(UserException):
    pass
