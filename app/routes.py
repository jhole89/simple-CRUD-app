from flask import render_template

from app import app


@app.route('/')
@app.route('/index')
def home():
    """
    API endpoint for home /
    :return: rendered index.html page
    """
    return render_template("index.html")
