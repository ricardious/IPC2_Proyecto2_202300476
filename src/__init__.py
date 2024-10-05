from flask import Flask

from .routes import main_routes

app = Flask(__name__)


def init_app(config):
    app.config.from_file(config)

    app.register_blueprint(main_routes.main_routes, url_prefix='/')

    return app
