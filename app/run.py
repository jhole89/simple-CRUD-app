# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response
import logging
from typing import *

app = Flask(__name__)


@app.route('/')
def home():
    """
    API endpoint for home /
    :return: rendered index.html page
    """
    return render_template("index.html")


if __name__ == '__main__':
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

app.run()
