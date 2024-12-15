import unittest
from flask import Flask, json
from src.app import app, mongo

class InventoryTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        mongo.db.products.delete_many({})

    def test_get_all_products(self):
        mongo.db.products.insert_one({
            'name': 'Product 1',
            'category': 'Category A',
            'quantity': 5,
            'price': 10.0
        })
        response = self.app.get('/products')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Product 1')

    def test_add_product(self):
        response = self.app.post('/products', json={
            'name': 'Product 2',
            'category': 'Category B',
            'price': 20.0
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product 2', data['name'])

    def test_update_product(self):
        product_id = mongo.db.products.insert_one({
            'name': 'Product 3',
            'category': 'Category A',
            'quantity': 8,
            'price': 30.0
        }).inserted_id
        response = self.app.put(f'/products/{product_id}', json={
            'quantity': 10,
            'price': 25.0
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['quantity'], 10)
        self.assertEqual(data['price'], 25.0)

    def test_delete_product(self):
        product_id = mongo.db.products.insert_one({
            'name': 'Product 4',
            'category': 'Category B',
            'quantity': 15,
            'price': 40.0
        }).inserted_id
        response = self.app.delete(f'/products/{product_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual