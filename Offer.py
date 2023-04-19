class Offer:
    def __init__(self, link, name, description, year, capacity, fuel, city, province, photo, price):
        self.link = link
        self.name = name
        self.description = description
        self.year = year
        self.capacity = capacity
        self.fuel = fuel
        self.city = city
        self.province = province
        self.photo = photo
        self.price = price

    def info(self):
        return f'${self.name} {self.price} (${self.link}): {self.description}, [{self.year},{self.capacity},{self.fuel}] //{self.city} ({self.province})// ({self.photo})'
