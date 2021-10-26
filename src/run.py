from flask import Flask

from conf import db


def register_extensions(app):
    db.init_app(app)
    app.app_context().push()

    from src.models import News
    db.create_all()


def create_app():
    app = Flask(__name__)
    register_extensions(app)
    return app
