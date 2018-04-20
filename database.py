import configparser
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

customers = None
products = None
orders = None

customer_keys = ('firstName', 'lastName', 'street', 'city', 'state', 'zip')
product_keys = ('name', 'price')
order_keys = ('customer', 'product')

# utility function you might find useful.. accepts a key list (see above) and 
# a document returned by pymongo (dictionary) and turns it into a list.     
def to_list(keys, document):
    record = []
    for key in keys:
        record.append(document[key])
    return record  

# utility function you might find useful...  Similar to to_list above, but it's appending
# to a list (record) instead of creating a new one.  Useful for when you already have a
# list, but need to join another dictionary object into it...
def join(keys, document, record):
    for key in keys:
        record.append(document[key])
    return record

# The following functions are REQUIRED - you should REPLACE their implementation
# with the appropriate code to interact with your Mongo database.
def initialize():
    global customers
    global products
    global orders

    config = configparser.ConfigParser()
    config.read('config.ini')
    connection_string = config['database']['mongo_connection']
    conn = MongoClient(connection_string)
    
    customers = conn.db_project2.customers
    products = conn.db_project2.products
    orders = conn.db_project2.orders

    # You might also want to connect to redis...

def get_customers():
    allCustomers = customers.find({})
    for customer in allCustomers:
        yield customer

def get_customer(id):
    return customers.find_one({'_id' : ObjectId(id)})

def upsert_customer(customer):
    customers.insert_one(customer)

def delete_customer(id):
    orders.delete_many({'customerId' : id})
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
    orders.insert_one(order)

def delete_order(id):
    orders.delete_one({'_id' :  ObjectId(id)})

# Pay close attention to what is being returned here.  Each product in the products
# list is a dictionary, that has all product attributes + last_order_date, total_sales, and 
# gross_revenue.  This is the function that needs to be use Redis as a cache.

# - When a product dictionary is computed, save it as a hash in Redis with the product's
#   ID as the key.  When preparing a product dictionary, before doing the computation, 
#   check if its already in redis!
def sales_report():
    return list()

initialize()