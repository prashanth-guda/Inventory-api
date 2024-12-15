from bson import ObjectId

class Product:
    def __init__(self, name, category, quantity=0, price=0.0):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price
        }

    @staticmethod
    def from_dict(data):
        return Product(
            name=data.get('name'),
            category=data.get('category'),
            quantity=data.get('quantity', 0),
            price=data.get('price')
        )
