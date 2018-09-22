from pony.orm import *
import json
import os

try:  
   username = os.environ.get("DB_USER")
   password = os.environ.get("DB_PASSWORD")
except KeyError: 
   print("Not exist environment value for %s" % "key_maybe_not_exist")

db = Database()
db.bind(provider='mysql', host='127.0.0.1', user=username, passwd=password, db='Shopify')

#Create tables
class Shop(db.Entity):
    name = Required(str)
    orders = Set('Order')
    product = Set('Product')

class Order(db.Entity):
    shop = Required(Shop)
    total = Required(int)
    lineItems = Set('LineItem')

class Product(db.Entity):
    name = Required(str)
    price = Required(int)
    shop = Required(Shop)
    quantity = Required(int)
    lineItems = Set('LineItem')

class LineItem(db.Entity):
    price = Required(int)
    quantity = Required(int)
    product = Required(Product)
    order = Required(Order)

db.generate_mapping(create_tables=True)

types = {
    'shop':db.Shop,
    'order':db.Order,
    'product':db.Product,
    'lineItem':db.LineItem
}

@db_session
def return_all(entity_type):
    entity_list = []
    entities =  select(entity for entity in types[entity_type])
    for entity in entities:
        entity_list.append(entity.to_dict())
    return entity_list

@db_session
def return_entity(id,type):
    return types[type][id].to_dict()

@db_session
def return_product(product_id = None, shop_id = None): 
    if product_id != None: 
        if shop_id == None: # Has product ID and no shop ID
            return Product[product_id].to_dict()
        else: # Has product ID and shop ID
            shop_list = []
            filtered_product_list =  select(product for product in db.Product if product.shop is Shop[shop_id] and product.id == product_id )
            for product in filtered_product_list:
                shop_list.append(product.to_dict())
            print(shop_list)
            return shop_list
    else:
        if shop_id != None:
            product_list = []
            filtered_product_list =  select(product for product in db.Product if product.shop == Shop[shop_id])
            for product in filtered_product_list:
                product_list.append(product.to_dict())
            return product_list

@db_session
def return_order(order_id = None, shop_id = None): 
    if order_id != None: 
        if shop_id == None: # Has Order ID and no shop ID
            return Order[order_id].to_dict()
        else: # Has Order ID and shop ID
            order_list = []
            filtered_order_list =  select(order for order in db.Order if order.shop is Shop[shop_id] and order.id == order_id )
            for order in filtered_order_list:
                order_list.append(order.to_dict())
            print(order_list)
            return order_list
    else:
        if shop_id != None:
            order_list = []
            filtered_order_list =  select(order for order in db.Order if order.shop == Shop[shop_id])
            for order in filtered_order_list:
                order_list.append(order.to_dict())
            return order_list

@db_session
def return_lineitem(order_id = None, product_id = None,lineitem_id=None): 
        if lineitem_id:
            return LineItem[lineitem_id].to_dict()
        else:
            if order_id != None:
                lineitem_list = []
                filtered_lineitem_list =  select(lineitem for lineitem in db.LineItem if lineitem.order == Order[order_id])
                for lineitem in filtered_lineitem_list:
                    lineitem_list.append(lineitem.to_dict())
                return lineitem_list
            else:
                lineitem_list = []
                filtered_lineitem_list =  select(lineitem for lineitem in db.LineItem if lineitem.product == Product[product_id])
                for lineitem in filtered_lineitem_list:
                    lineitem_list.append(lineitem.to_dict())
                return lineitem_list

            


@db_session
def delete_entity(id,type):
    types[type][id].delete()

@db_session
def add_shop(name,id=None):
    if(Shop.get(id=id)):
        Shop[id].name = name
    Shop(name=name)

@db_session
def add_product(name,price,shop,quantity,id=None):
    if(Product.get(id=id)):
        Product[id].name = name
        Product[id].price = price
        Product[id].shop = shop
        Product[id].quantity = quantity
    Product(name=name,price=price,shop=shop,quantity=quantity)

@db_session
def add_order(shop,id=None):
    if(Order.get(id=id)):
        Order[id].shop = shop
        return
    Order(shop=shop,total=0)

@db_session
def add_line_item(order,product,quantity,id=None):
    quantity = int(quantity)
    if int(Product[product].quantity) - quantity > 0:
        Product[product].quantity -= quantity
        price = int(Product[product].price)
        if(LineItem.get(id=id)):
            LineItem[id].order = order
            LineItem[id].product = product
            LineItem[id].quantity = quantity
            LineItem[id].price = price
        LineItem(quantity=quantity,order=order,product=product,price=price)
        Order[order].total += quantity*price #Update total 
        return 'Line Item has been added',200
    else:
        return 'Insufficient stock in warehouse',300

@db_session
def add_test_data():
    shop1 = Shop(name='FouseyTube')
    shop2 = Shop(name='Kylie Jenner')
    shop3 = Shop(name='Logan Paul')
    shop4 = Shop(name='Costco')
    product1 = Product(price=43,shop=shop3,name="Maverick Hoodie",quantity=500)
    product2 = Product(price=50,shop=shop1,name="Best Family on youtube t-shirt",quantity=200)
    product3 = Product(price=400,shop=shop2,name="Brown Lipstick",quantity=50)
    order1 = Order(shop=shop1,total=0)
    order2 = Order(shop=shop3,total=0)
    lineitem1 = LineItem(product=2,order=4,quantity=20,price=50)
    lineitem1 = LineItem(product=5,order=5,quantity=24,price=300)

    # Add quantity to the products
    commit()

@db_session 
def query(self):
    products = select(p for p in db.Product if p.price > 20)[:]
    for product in products:
        print(product.to_dict())


    add_test_data()