#!/usr/bin/python3
"""index Module"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON with status: Ok"""
    return jsonify({"status": "OK"}), 200
