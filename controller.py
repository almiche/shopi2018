from flask import Flask
import asyncio
from flask import jsonify, request
from flask_cors import CORS
from registry import *
from pony.flask import Pony


class Controller():

    def __init__(self):
        self.app = Flask(__name__,static_url_path='')
        CORS(self.app)
        self.app.config['SECRET_KEY'] = 'secret'
        self.register_routes()
        self.app.run(host="0.0.0.0",port=9292,debug=True)
        Pony(self.app)

    
    def register_routes(self):
        @self.app.route('/')
        def index():
            add_test_data()
            return '',200

        @self.app.route('/api/v1.0/shops/<id>', methods=['GET','PUT','DELETE'])
        @self.app.route('/api/v1.0/shops/', methods=['GET','PUT'])
        def handle_shop_requests(id = None):
            try:
                if request.method == 'GET':
                    if id != None:
                            return jsonify(return_entity(id,'shop')),200
                    return jsonify(return_all('shop')),200

                if request.method == 'PUT':
                    add_shop(request.json['name'],id)
                    return '',200

                #TODO add verification of deletion
                if request.method == 'DELETE':
                    delete_shop(id)
                    return '',200

            except pony.orm.core.ObjectNotFound:
                return " ", 404

            return 'Method not allowed',500

        @self.app.route('/api/v1.0/shops/<shop_id>/products/<product_id>', methods=['GET','PUT','DELETE'])
        @self.app.route('/api/v1.0/shops/<shop_id>/products', methods=['GET','PUT'])
        def handle_product_requests(product_id = None, shop_id = None):
            try:
                if request.method == 'GET':
                    return jsonify(return_product(product_id,shop_id))
                if request.method == 'PUT':
                    print(request.json)
                    add_product(request.json['name'],request.json['price'],shop_id,request.json['quantity'],product_id)
                    return '',200
                if request.method == 'DELETE':
                    delete_product(shop_id,product_id)
                    return '',200

            except pony.orm.core.ObjectNotFound:
                return " ", 404
            return '',500

        @self.app.route('/api/v1.0/shops/<shop_id>/orders/<order_id>', methods=['GET','DELETE'])
        @self.app.route('/api/v1.0/shops/<shop_id>/orders', methods=['GET','PUT'])
        def handle_order_requests(order_id = None, shop_id = None):
            try:
                if request.method == 'GET':
                    return jsonify(return_order(order_id,shop_id))
                if request.method == 'PUT':
                    add_order(shop_id,order_id)
                    return '',200
                if request.method == 'DELETE':
                    delete_order(shop_id,order_id)
                    return '',200

            except pony.orm.core.ObjectNotFound:
                return " ", 404
            return '',500       

        @self.app.route('/api/v1.0/shops/<shop_id>/orders/<order_id>/lineitems/<lineItem_id>', methods=['GET','PUT','DELETE'])
        @self.app.route('/api/v1.0/shops/<shop_id>/orders/<order_id>/lineitems', methods=['GET'])
        @self.app.route('/api/v1.0/shops/<shop_id>/products/<product_id>/lineitems', methods=['GET','PUT'])
        @self.app.route('/api/v1.0/shops/<shop_id>/products/<product_id>/lineitems/<lineItem_id>', methods=['GET','PUT','DELETE'])
        def handle_lineitem_requests(shop_id,order_id = None, product_id = None, lineItem_id=None):
            try:
                if request.method == 'GET':
                    return jsonify(return_lineitem(shop_id,order_id,product_id,lineItem_id))
                if request.method == 'PUT':
                    if order_id:
                        add_line_item(order_id,request.json['product'],request.json['quantity'],lineItem_id)
                        return '',200
                    if product_id:
                        add_line_item(request.json['order'],product_id,request.json['quantity'],lineItem_id)
                        return '',200
                if request.method == 'DELETE':
                    delete_lineitem(order_id,product_id,lineItem_id)
                    return '',200

            except pony.orm.core.ObjectNotFound:
                return " ", 404
            return '',500      


if __name__ == '__main__':
    Controller()