"""Flask web application factory."""

import os

from dotenv import load_dotenv
from flask import Flask

from web_app.routes.home_routes import home_routes
from web_app.routes.rps_routes import rps_routes
from web_app.routes.stocks_routes import stocks_routes

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", default="dev-only-secret")  # set a real value in production


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.register_blueprint(home_routes)
    app.register_blueprint(rps_routes)
    app.register_blueprint(stocks_routes)
    return app


if __name__ == "__main__":
    create_app().run(debug=True)
