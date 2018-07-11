# tests/test_views.py
from flask_testing import TestCase
import json
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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Socialive.tv')
        self.assertEqual(response.json['id'], 2)

    def test_product_unit_not_found(self):
        response = self.client.get("/api/v1/products/89087654")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Product not found')

    def test_delete_product_not_found(self):
        response = self.client.delete("/api/v1/products/89087654")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Product not found')

    def test_delete_product_work(self):
        response = self.client.delete("/api/v1/products/3")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.json, None)
        response_get = self.client.get("/api/v1/products/3")
        self.assertEqual(response_get.status_code, 404)
        self.assertEqual(response_get.json['error'], 'Product not found')

    def test_add_product_work(self):
        payload = { 'name': 'Fakeproduct' }
        response = self.client.post("/api/v1/products", data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Fakeproduct')

    def test_add_product_fail(self):
        payload = { 'name': 'Fakeproduct2' }
        self.client.post("/api/v1/products", data=json.dumps(payload))
        response = self.client.post("/api/v1/products", data=json.dumps(payload))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json['error'], "Product already exists")

    def test_add_product_payload_missing_param(self):
        payload = { 'youpi': 'Fakeproduct3' }
        self.client.post("/api/v1/products", data=json.dumps(payload))
        response = self.client.post("/api/v1/products", data=json.dumps(payload))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json['error'], "Bad payload received")
