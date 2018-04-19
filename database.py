


# The following functions are REQUIRED - you should REPLACE their implementation
# with the appropriate code to interact with your Mongo database.
def initialize():
    # this function will get called once, when the application starts.
    # this would be a good place to initalize your connection!
    # You might also want to connect to redis...
    print('Nothing to do here...')

def get_customers():
    return list()

def get_customer(id):
    return None

def upsert_customer(customer):
    return None


def delete_customer(id):
    return None

    
def get_products():
    return list()

def get_product(id):
    return None

def upsert_product(product):
    return None

def delete_product(id):
    return None

def get_orders():
    return list()

def get_order(id):
    return None

def upsert_order(order):
    return None

def delete_order(id):
    return None


# Pay close attention to what is being returned here.  Each product in the products
# list is a dictionary, that has all product attributes + last_order_date, total_sales, and 
# gross_revenue.  This is the function that needs to be use Redis as a cache.

# - When a product dictionary is computed, save it as a hash in Redis with the product's
#   ID as the key.  When preparing a product dictionary, before doing the computation, 
#   check if its already in redis!
def sales_report():
    return list()
