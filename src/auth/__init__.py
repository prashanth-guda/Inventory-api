from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.inventory
products = [
    {'name': 'Product 1', 'category': 'Category A', 'quantity': 5, 'price': 10.0},
    {'name': 'Product 2', 'category': 'Category B', 'quantity': 15, 'price': 20.0},
    {'name': 'Product 3', 'category': 'Category A', 'quantity': 8, 'price': 30.0},
]
db.products.insert_many(products)
print("Database initialized with sample data")
