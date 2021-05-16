class Card:
    def __init__(self, card_id, password, owner_id, balance):
        self.card_id = card_id
        self.password = password
        self.owner_id = owner_id
        self.balance = balance

    def display(self):
        card_feature = {'Card ID': self.card_id, 'Owner ID': self.owner_id,
                        'Balance': str(self.balance)}
        return card_feature
