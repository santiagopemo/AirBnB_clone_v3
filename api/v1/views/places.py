#!/usr/bin/python3
"""places Module"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """Retrieves the list of all places in a city objects"""
    city = storage.get(City, city_id)
    places_list = []
    if city is None:
        abort(404)
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_by_id(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place in a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_dict:
        abort(400, 'Missing user_id')
    if 'name' not in request_dict:
        abort(400, 'Missing name')
    user_id = request_dict['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in request_dict:
        abort(400, 'Missing name')
    place = Place(**request_dict)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for key, value in request_dict.items():
        if key != 'id' and key != 'user_id' and key != 'city_id' \
                    and key != 'created_at' and key != 'updated_at':
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
