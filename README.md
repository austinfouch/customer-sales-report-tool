# Customer and Sales Report Tool
This application is very simply an order database. It provides the ability to add generic products, customers, and orders, as well as displaying customer and sales reports.

To run:
  - `$ git clone https://github.com/austinfouch/customer-sales-report-tool`
  - `$ cd ..\customer-sales-report-tool`
  - Create a config.ini file of the following format:
    ```
    [database]
    mongo_connection = <mongodb-url>
    redis_host = <redis-url>
    redis_port = <redis-port>
    redis_pw = <redis-pw>
    ```
  - Note: be sure to replace the right hand values with the appropriate values from your MongoDB and Redis databases.
  - Set flask environment variable `FLASK_APP='pcs.py'`
  - `$ flask run`
  - Navigate to `http://localhost:5000/` in your browser
  
Dependencies:
  - flask
  - configparser
  - redis
  - pymongo
