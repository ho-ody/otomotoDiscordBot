class Offer:
    def __init__(self, link, name, description, year, mileage, capacity, fuel, city, province, date, photo, price):
        self.link = link
        self.name = name
        self.description = description
        self.year = year
        self.mileage = mileage
        self.capacity = capacity
        self.fuel = fuel
        self.city = city
        self.province = province
        self.date = date
        self.photo = photo
        self.price = price

    def __eq__(self, other):
        """Overrides the default implementation"""
        if self.link == other.link:
            return True
        return False

    def info(self):
        return f'[{self.date}] {self.name} --> {self.price} {self.mileage} ({self.link}): {self.description}, [{self.year},{self.capacity},{self.fuel}] //{self.city} ({self.province})// ({self.photo})'
