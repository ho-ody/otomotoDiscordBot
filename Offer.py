class Offer:
    def __init__(self, link, name, description, year, capacity, fuel):
        self.link = link
        self.name = name
        self.description = description
        self.year = year
        self.capacity = capacity
        self.fuel = fuel

    def info(self):
        return f'${self.name} (${self.link}): {self.description}, [{self.year},{self.capacity},{self.fuel}]'
