class User:
    def __init__(self, category, user_id, name_surname, owned_item, reserved_item, card_id, email):
        self.category = category
        self.user_id = user_id  # int
        self.name_surname = name_surname
        self.owned_item = owned_item  # int
        self.reserved_item = reserved_item  # int
        self.card_id = card_id  # int
        self.email = email

    def display(self):
        feature_list = (self.category, str(self.user_id), str(self.card_id), self.email)
        return feature_list
