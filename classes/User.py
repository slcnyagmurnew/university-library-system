class User:
    def __init__(self, category, user_id, name_surname, owned_item, reserved_item, owned_id_list, card_id, email):
        self.category = category
        self.user_id = user_id  # int
        self.name_surname = name_surname
        self.owned_item = owned_item  # int
        self.reserved_item = reserved_item  # int
        self.owned_id_list = owned_id_list  # string
        self.card_id = card_id  # int
        self.email = email

    def display(self):
        feature_list = {'Category': self.category, 'User ID': str(self.user_id), 'Name Surname': self.name_surname,
                        'Number of Owned Items': str(self.owned_item), 'Number of Reserved Items': str(self.reserved_item),
                        'Owned Items ID List': self.owned_id_list, 'Card ID': str(self.card_id), 'Email': self.email}
        return feature_list
