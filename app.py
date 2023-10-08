from flask import Flask
from flask_cors import CORS

from config import BaseConfig


def create_app(config=None):
    app = Flask(BaseConfig.PROJECT, instance_relative_config=True)

    configure_app(app, config)

    return app


def configure_app(app, config=None):
    app.config.from_object(config or BaseConfig)

    from views import blueprint
    app.register_blueprint(blueprint)

    CORS(app)



