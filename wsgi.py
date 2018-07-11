# wsgi.py
from flask import Flask
from flask import jsonify
app = Flask(__name__)

the_products = [
        { 'id': 1, 'name': 'Skello' },
        { 'id': 2, 'name': 'Socialive.tv' },
        { 'id': 3, 'name': 'Scality' },
        { 'id': 4, 'name': 'Actifio' }
    ]

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def products():
    return jsonify(the_products)

@app.route('/api/v1/products/<id>')
def product(id):
    for product in the_products:
        if product['id'] == int(id):
            return jsonify(product)
    return jsonify({'error' : 'Product not found'}), 404
