class Game:

    def __init__(self):
        self.name = ""
        self.price = 0
        self.new_price = 0

    def is_discount(self):
        if self.new_price < self.price:
            return True
        return False

    def __str__(self):
        return f"{self.name}\nCurrent price: {self.new_price}\nRegular price: {self.price}\n"