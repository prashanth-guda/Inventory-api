from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Product
from app import mongo
from bson.objectid import ObjectId

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    query = {}
    if 'category' in request.args:
        query['category'] = request.args['category']
    products = mongo.db.products.find(query)
    if 'sort' in request.args:
        sort_order = 1 if request.args['sort'] == 'asc' else -1
        products = products.sort('price', sort_order)
    products_list = []
    for product in products:
        product['_id'] = str(product['_id'])
        product['low_stock'] = product['quantity'] < 10
        products_list.append(product)
    return jsonify(products_list), 200

@product_bp.route('/products/<product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if product:
        product['_id'] = str(product['_id'])
        product['low_stock'] = product['quantity'] < 10
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.json
    if not data.get('name') or not data.get('category') or not data.get('price'):
        return jsonify({"error": "Missing required fields"}), 400
    new_product = Product.from_dict(data)
    product_id = mongo.db.products.insert_one(new_product.to_dict()).inserted_id
    new_product_dict = new_product.to_dict()
    new_product_dict['_id'] = str(product_id)
    return jsonify(new_product_dict), 201

@product_bp.route('/products/<product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    data = request.json
    update_data = {}
    if 'quantity' in data and data['quantity'] < 0:
        return jsonify({"error": "Quantity cannot be negative"}), 400
    if 'quantity' in data:
        update_data['quantity'] = data['quantity']
    if 'price' in data:
        update_data['price'] = data['price']
    mongo.db.products.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    updated_product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    updated_product['_id'] = str(updated_product['_id'])
    updated_product['low_stock'] = updated_product['quantity'] < 10
    return jsonify(updated_product), 200

@product_bp.route('/products/<product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    result = mongo.db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 1:
        return jsonify({"message": "Product deleted"}), 200
    return jsonify({"error": "Product not found"}), 404

@product_bp.route('/metrics', methods=['GET'])
@jwt_required()
def get_metrics():
    total_products = mongo.db.products.count_documents({})
    average_price = mongo.db.products.aggregate([{"$group": {"_id": None, "average_price": {"$avg": "$price"}}}])
    low_stock_count = mongo.db.products.count_documents({"quantity": {"$lt": 10}})
    return jsonify({
        "total_products": total_products,
        "average_price": list(average_price)[0]['average_price'] if average_price else 0,
        "low_stock_count": low_stock_count
    }), 200
