from flask import Flask
import asyncio
from flask import jsonify, request, render_template
from flask_cors import CORS
from registry import *
from pony.flask import Pony
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask_hashing import Hashing
import secrets


class Controller():

    def __init__(self):
        self.app = Flask(__name__)
        self.hashing = Hashing(self.app)
        CORS(self.app)
        self.app.config['SECRET_KEY'] = 'secret'
        self.register_routes()
        self.app.run(host="0.0.0.0",port=9292,debug=True)
        Pony(self.app)

    def verify_api_token(self,id,token):
        user = return_salt_and_stores(id)
        if self.hashing.check_value(user[0], token, salt=user[1]):
           return True
        else:
            return False
    
    def register_routes(self):
        @self.app.route('/')
        def index():
            return render_template("sign_up.html"),200

        @self.app.route('/sign-up',methods=['POST'])
        def sign_up():
            if request.method == "POST":
                password = request.json['Password']
                stores = []
                for store in request.json['Stores']:
                    stores.append(store)
                salt = secrets.token_hex(nbytes=16)
                hash = self.hashing.hash_value(password, salt=salt)
                id = create_api_token(hash,stores,salt)
            return 'Your user has been created! Make sure to add field id {} with your api password in your requests'.format(id),200

        @self.app.route('/api/v1.0/shops/<shop_id>', methods=['GET','PUT','DELETE'])
        @self.app.route('/api/v1.0/shops/', methods=['GET','PUT'])
        def handle_shop_requests(shop_id = None):
            try:
                if request.method == 'GET':
                    if shop_id != None:
                            return jsonify(return_entity(shop_id,'shop')),200
                    return jsonify(return_all('shop')),200

                if request.method == 'PUT':
                    if self.verify_api_token(request.json['id'],request.json['token']):
                        add_shop(request.json['name'],shop_id)
                        return '',200
                    else:
                        return 'You are not authorized in this are', 500

                if request.method == 'DELETE':
                    if self.verify_api_token(request.json['id'],request.json['token']):
                        delete_shop(id)
                        return '',200
                    else:
                        return 'You are not authorized in this are', 500

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
                    if self.verify_api_token(request.json['id'],request.json['token']):
                        add_product(request.json['name'],request.json['price'],shop_id,request.json['quantity'],product_id)
                        return '',200
                    else:
                        return 'You are not authorized in this are', 500
                if request.method == 'DELETE':
                    if self.verify_api_token(request.json['id'],request.json['token']):
                        delete_product(shop_id,product_id)
                        return '',200
                    else:
                        return 'You are not authorized in this are', 500

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
                    if self.verify_api_token(request.json['id'],request.json['token']):
                        add_order(shop_id,order_id)
                        return '',200
                    else:
                        return 'You are not authorized in this are', 500
                if request.method == 'DELETE':
                    if self.verify_api_token(request.json['id'],request.json['token']):
                        delete_order(shop_id,order_id)
                        return '',200
                    else:
                        return 'You are not authorized in this are', 500

            except pony.orm.core.ObjectNotFound:
                return " ", 404
            return '',500       

        @self.app.route('/api/v1.0/shops/<shop_id>/orders/<order_id>/lineitems/<lineItem_id>', methods=['GET','PUT','DELETE'])
        @self.app.route('/api/v1.0/shops/<shop_id>/orders/<order_id>/lineitems', methods=['GET','PUT'])
        @self.app.route('/api/v1.0/shops/<shop_id>/products/<product_id>/lineitems', methods=['GET','PUT'])
        @self.app.route('/api/v1.0/shops/<shop_id>/products/<product_id>/lineitems/<lineItem_id>', methods=['GET','PUT','DELETE'])
        def handle_lineitem_requests(shop_id,order_id = None, product_id = None, lineItem_id=None):
            try:
                if request.method == 'GET':
                    return jsonify(return_lineitem(shop_id,order_id,product_id,lineItem_id))
                if request.method == 'PUT':
                    if self.verify_api_token(request.json['id'],request.json['token']):
                        if order_id:
                            add_line_item(order_id,request.json['product'],request.json['quantity'],lineItem_id)
                            return '',200
                        if product_id:
                            add_line_item(request.json['order'],product_id,request.json['quantity'],lineItem_id)
                            return '',200
                    else:
                        return 'You are not authorized in this are', 500
                if request.method == 'DELETE':
                    if self.verify_api_token(request.json['id'],request.json['token']):
                        delete_lineitem(order_id,product_id,lineItem_id)
                        return '',200
                    else:
                        return 'You are not authorized in this are', 500

            except pony.orm.core.ObjectNotFound:
                return " ", 404
            return '',500      


if __name__ == '__main__':
    Controller()