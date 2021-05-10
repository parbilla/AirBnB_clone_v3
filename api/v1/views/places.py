#!/usr/bin/python3
"""New view for Places objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getPlace1(place_id=None):
    """Defines get method 1"""
    objName = "Place." + place_id
    if (objName in storage.all()):
        return jsonify((storage.get(Place, place_id)).to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getPlace2(city_id=None):
    """defines get method 2"""
    if (("City." + city_id) in storage.all()):
        places = []
        for place in storage.all("Place").values():
            places.append(place.to_dict())
        return jsonify(places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    """Defines delete method"""

    objName = "Place." + place_id
    if objName in storage.all():
        storage.get(Place, place_id).delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def postPlace(city_id=None):
    """Defines post method"""

    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    if storage.get(City, city_id) is None:
        abort(404)
    if storage.get(User, request.get_json()['user_id']) is None:
        abort(404)
    request.get_json()['city_id'] = city_id
    newPlace = Place(**request.get_json())
    newPlace.save()
    return (jsonify(newPlace.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def putPlace(place_id):
    """Defines put method"""

    if not request.get_json():
        abort(400, 'Not a JSON')
    objName = "Place." + place_id
    if (objName in storage.all()):
        newPlace = storage.get(Place, place_id)
        changePlace = request.get_json()
        for key, value in changePlace.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(newPlace, key, value)
        newPlace.save()
        return (jsonify(newPlace.to_dict()), 200)
    else:
        abort(404)
