# Customer and Sales Report Tool
This application is very simply an order database. It provides the ability to add generic products, customers, and orders, as well as displaying customer and sales reports.

To run:
  1. `$ git clone https://github.com/austinfouch/customer-sales-report-tool`
  2. `$ cd ..\customer-sales-report-tool`
  3. Create a config.ini file of the following format:
    <p>`[database]`</p>
    <p>`mongo_connection = <mongodb-url>`</p>
    <p>`redis_host = <redis-url>`</p>
    <p>`redis_port = <redis-port>`</p>
    <p>`redis_pw = <redis-pw>`</p>
  3. Set flask environment variable `FLASK_APP='pcs.py'`
  4. `$ flask run`
  5. Navigate to `http://localhost:5000/` in your browser
  
Dependencies:
  - flask
  - configparser
  - redis
  - pymongo
