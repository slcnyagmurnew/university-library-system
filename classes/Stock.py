class Stock:
    def __init__(self, category, kind, name, creator, item_id, date, shelf, available):
        self.name = name
        self.category = category
        self.kind = kind
        self.creator = creator
        self.item_id = item_id
        self.date = date
        self.shelf = shelf
        self.available = available

    def display(self, category, kind, name, creator, item_id, date, shelf, available):
        self.name = name
        self.category = category
        self.kind = kind
        self.creator = creator
        self.item_id = item_id
        self.date = date
        self.shelf = shelf
        self.available = available
