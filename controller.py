from flask import Flask
import asyncio
from flask import jsonify, request
from flask_cors import CORS
from registry import *
from pony.flask import Pony
import pry


class Controller():

    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.config['SECRET_KEY'] = 'secret'
        self.dhcp_config = {}
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
                    add_shop(request.form['name'],id)
                    return '',200

                #TODO add verification of deletion
                if request.method == 'DELETE':
                    delete_entity(id,'shop')
                    return '',200

            except pony.orm.core.ObjectNotFound:
                return " ", 404

            return 'Method not allowed',500

        @self.app.route('/api/v1.0/shops/<shop_id>/products/<product_id>', methods=['GET','PUT','DELETE'])
        @self.app.route('/api/v1.0/products/<product_id>',methods=['GET','PUT','DELETE'])
        @self.app.route('/api/v1.0/shops/<shop_id>/products', methods=['GET','PUT'])
        @self.app.route('/api/v1.0/products', methods=['PUT'])
        def handle_product_requests(product_id = None, shop_id = None):
            try:
                if request.method == 'GET':
                    return jsonify(return_product(product_id,shop_id))
                if request.method == 'PUT':
                    if shop_id != None:
                        add_product(request.form['name'],request.form['price'],shop_id,request.form['quantity'],product_id)
                        return '',200
                    else:
                        add_product(request.form['name'],request.form['price'],request.form['shop'],request.form['quantity'],product_id)
                        return '',200
                if request.method == 'DELETE':
                    delete_entity(product_id,'product')
                    return '',200

            except pony.orm.core.ObjectNotFound:
                return " ", 404
            return '',500

        @self.app.route('/api/v1.0/shops/<shop_id>/orders/<order_id>', methods=['GET','PUT','DELETE'])
        @self.app.route('/api/v1.0/orders/<order_id>',methods=['GET','PUT','DELETE'])
        @self.app.route('/api/v1.0/shops/<shop_id>/orders', methods=['GET','PUT'])
        @self.app.route('/api/v1.0/orders', methods=['PUT'])
        def handle_order_requests(order_id = None, shop_id = None):
            try:
                if request.method == 'GET':
                    return jsonify(return_order(order_id,shop_id))
                if request.method == 'PUT':
                    if shop_id != None:
                        add_order(shop_id,order_id)
                        return '',200
                    else:
                        add_order(request.form['shop'],order_id)
                        return '',200
                if request.method == 'DELETE':
                    delete_entity(order_id,'order')
                    return '',200

            except pony.orm.core.ObjectNotFound:
                return " ", 404
            return '',500       

        @self.app.route('/api/v1.0/orders/<order_id>/lineitems/<lineItem_id>', methods=['GET','PUT','DELETE'])
        @self.app.route('/api/v1.0/orders/<order_id>/lineitems', methods=['GET'])
        @self.app.route('/api/v1.0/lineitems/<lineItem_id>',methods=['GET','PUT','DELETE'])
        @self.app.route('/api/v1.0/products/<product_id>/lineitems', methods=['GET','PUT'])
        @self.app.route('/api/v1.0/products/<product_id>/lineitems/<lineItem_id>', methods=['GET','PUT'])
        def handle_lineitem_requests(order_id = None, product_id = None, lineItem_id=None):
            try:
                if request.method == 'GET':
                    return jsonify(return_lineitem(order_id,product_id,lineItem_id))
                if request.method == 'PUT':
                    if order_id:
                        add_line_item(order_id,request.form['product'],request.form['quantity'],lineItem_id)
                        return '',200
                    if product_id:
                        add_line_item(request.form['order'],product_id,request.form['quantity'],lineItem_id)
                        return '',200
                if request.method == 'DELETE':
                    delete_entity(lineItem_id,'lineitem')
                    return '',200

            except pony.orm.core.ObjectNotFound:
                return " ", 404
            return '',500      


if __name__ == '__main__':
    Controller()