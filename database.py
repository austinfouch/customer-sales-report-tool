import configparser
import redis
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

customers = None
products = None
orders = None
redisCache = None

def initialize():
    global customers
    global products
    global orders
    global redisCache

    config = configparser.ConfigParser()
    config.read('config.ini')

    mongoConnStr = config['database']['mongo_connection']
    mongoConn = MongoClient(mongoConnStr)
    customers = mongoConn.db_project2.customers
    products = mongoConn.db_project2.products
    orders = mongoConn.db_project2.orders

    redisCache = redis.StrictRedis(host=config['database']['redis_host'],
                                port=config['database']['redis_port'],
                                password=config['database']['redis_pw'],
                                db=0,
                                decode_responses=True)
    redisCache.flushdb()

def get_customers():
    allCustomers = customers.find({})
    for customer in allCustomers:
        yield customer

def get_customer(id):
    return customers.find_one({'_id' : ObjectId(id)})

def upsert_customer(customer):
    customers.insert_one(customer)

def delete_customer(id):
    # must delete every order, and thus product in cache, associated with customer
    for order in get_orders():
        if order['customerId'] == id:
            orders.delete_one({'customerId' : id})
            redisCache.delete(ObjectId(order['productId']))
    customers.delete_one({'_id' : ObjectId(id)})
    
def get_products():
    allProducts = products.find({})
    for product in allProducts:
        yield product

def get_product(id):
    return products.find_one({'_id' : ObjectId(id)})

def upsert_product(product):
    products.insert_one(product)

def delete_product(id):
    orders.delete_many({'productId' :  id})
    redisCache.delete(ObjectId(id))
    products.delete_one({'_id' :  ObjectId(id)})

def get_orders():
    allOrders = orders.find({})
    for order in allOrders:
        yield order

def get_order(id):
    return orders.find_one({'_id' : ObjectId(id)})

def upsert_order(order):
    order['customer'] = get_customer(order['customerId'])
    order['product'] = get_product(order['productId'])
    redisCache.delete(ObjectId(order['productId']))
    orders.insert_one(order)

def delete_order(id):
    order = get_order(id)
    orders.delete_one({'_id' :  order['_id']})
    redisCache.delete(ObjectId(order['productId']))

def sales_report():
    sales = []
    for product in get_products():
        if redisCache.hgetall(product['_id']):
            sales.append(redisCache.hgetall(product['_id']))
        else:
            orders = [o for o in get_orders() if ObjectId(o['productId']) == product['_id']]
            orders = sorted(orders, key=lambda k: k['date'])
            if len(orders) > 0:
                product['last_order_date'] = orders[-1]['date']
            product['total_sales'] = len(orders)
            product['gross_revenue'] = product['price'] * product['total_sales']
            redisCache.hmset(product['_id'], product)
            sales.append(product)
    return sales