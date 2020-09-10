#!/usr/bin/python3
"""users Module"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    if 'email' not in request_dict:
        abort(400, 'Missing email')
    if 'password' not in request_dict:
        abort(400, 'Missing password')
    user = User(**request_dict)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, value in request_dict.items():
        if key != 'id' and key != 'email' and key != 'created_at'\
                                            and key != 'updated_at':
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
