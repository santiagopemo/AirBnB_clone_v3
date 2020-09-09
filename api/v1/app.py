#!/usr/bin/python3
"""app Module"""
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from os import getenv
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close_storage(self):
    """Calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=int(getenv('HBNB_API_PORT ', default='5000'))
    )
