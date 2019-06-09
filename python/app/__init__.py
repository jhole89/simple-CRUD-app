# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(class_config: Config = Config):
    app.config.from_object(class_config)
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    return app


from app import controllers, models
