class UserId:
    def __init__(self, user_id):
        self.user_id: str = str(user_id)

    def __eq__(self, other):
        return self.user_id == str(other)
