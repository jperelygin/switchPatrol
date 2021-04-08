class Game:

    def __init__(self):
        self.name = ""
        self.price = 0.0
        self.new_price = 0.0
        self.presence = False

    def is_discount(self):
        if self.new_price < self.price:
            return True
        return False

    def __str__(self):
        if self.is_discount():
            return f"{self.name}\nCurrent price: {self.new_price} RUB. <-- SALE!\nRegular price: {self.price} RUB.\n"
        else:
            return f"{self.name}\nCurrent price: {self.new_price} RUB.\nRegular price: {self.price} RUB.\n"