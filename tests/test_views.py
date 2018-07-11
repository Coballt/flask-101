# tests/test_views.py
from flask_testing import TestCase
from wsgi import app

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_products_json(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 3) # 3 is not a mistake here.

    def test_product_unit_works(self):
        response = self.client.get("/api/v1/products/2")
        product = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Socialive.tv')
        self.assertEqual(response.json['id'], 2)

    def test_product_unit_not_found(self):
        response = self.client.get("/api/v1/products/89087654")
        product = response.json
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Product not found')
