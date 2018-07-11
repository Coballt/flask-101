# wsgi.py
from flask import Flask
from flask import jsonify
from flask import request
import json
app = Flask(__name__)

the_products = [
        { 'id': 1, 'name': 'Skello' },
        { 'id': 2, 'name': 'Socialive.tv' },
        { 'id': 3, 'name': 'Scality' },
        { 'id': 4, 'name': 'Actifio' },
        { 'id': 5, 'name': 'Google' },
    ]

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def products():
    return jsonify(the_products)

@app.route('/api/v1/products/<int:id>', methods=['GET'])
def get_product(id):
    for product in the_products:
        if product['id'] == int(id):
            return jsonify(product)
    return jsonify({'error' : 'Product not found'}), 404

@app.route('/api/v1/products/<int:id>', methods=['DELETE'])
def del_product(id):
    for product in the_products:
        if product['id'] == id:
            del the_products[the_products.index(product)]
            return '', 204
    return jsonify({'error' : 'Product not found'}), 404

@app.route('/api/v1/products', methods=['POST'])
def add_product():
    try:
        payload = json.loads(request.data)
    except ValueError :
        return jsonify({"error" : "Bad payload received"}), 422
    if 'name' not in payload:
        return jsonify({"error" : "Bad payload received"}), 422
    max_id = 0
    for product in the_products:
        if max_id < product['id']:
            max_id = product['id']
        if product['name'] == payload['name']:
            return jsonify({"error" : "Product already exists"}), 422
    the_products.append({ 'id': max_id+1, 'name': payload['name'] })
    return jsonify({ 'id': max_id+1, 'name': payload['name'] }), 201

@app.route('/api/v1/products/<int:id>', methods=['PATCH'])
def change_product(id):
    try:
        payload = json.loads(request.data)
    except ValueError :
        return jsonify({"error" : "Bad payload received"}), 422
    if 'name' not in payload:
        return jsonify({"error" : "Bad payload received"}), 422
    for product in the_products:
        if product['id'] == id:
            product['name'] = payload['name']
            return '', 204
    return jsonify({'error' : 'Product not found'}), 404
