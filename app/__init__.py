# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

from app import controllers, models
