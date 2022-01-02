from flask import Flask

from database import db_session
from routing_methods import route_config


class FlaskAppWrapper(object):

    def __init__(self, app, **configs):
        self.app = app
        self.configs(**configs)

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)


flask_app = Flask(__name__)

@flask_app.teardown_request
def remove_session(ex=None):
    db_session.remove()


app = FlaskAppWrapper(flask_app)

# add all routing methods to app.endpoint
for route in route_config:
    app.add_endpoint( endpoint=route['endpoint'],
                      endpoint_name=route['endpoint_name'],
                      handler=route['handler'],
                      methods=route['methods']
                      )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
