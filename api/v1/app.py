#!/usr/bin/python3
"""app Module"""
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from os import getenv
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
host = getenv("HBNB_API_HOST") or '0.0.0.0'
port = getenv("HBNB_API_PORT") or 5000


@app.teardown_appcontext
def close_storage(self):
    """Calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Returns a JSON-formatted 404 status code response"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
