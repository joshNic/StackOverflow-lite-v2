from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    return app
