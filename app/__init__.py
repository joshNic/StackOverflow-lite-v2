from instance.config import DevelopmentConfig
from flask import Flask
from instance.config import TestingConfig


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig)

    return app
