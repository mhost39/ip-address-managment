## decryption of Routing and how work

#### ``` routing_methods.py ``` file 
- contain all route methods for routing
- for create a new rout method:

    add your methods then add new index in ``` route_config ``` list in this format:
   
    ``` { "endpoint" : "/endpoint", "endpoint_name" : "endpoint_name", "handler" : method_name, "methods" : ['POST/GET/...']} ```

#### ``` app.py ``` file 
- create a FlaskAppWrapper class
- create a new app
- add all routing methods to app.endpoint
- run app