#!/usr/bin/python3
"""New view for Cities objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getCity(city_id=None):
    """Defines get method 1"""
    objName = "City." + city_id
    if (objName in storage.all()):
        return jsonify((storage.get(City, city_id)).to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getCity2(state_id=None):
    """defines get method 2"""
    if (("State." + state_id) in storage.all()):
        cities = []
        for city in storage.all("City").values():
            if (city.state_id == state_id):
                print(city)
                cities.append(city.to_dict())
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteCity(city_id):
    """Defines delete method"""

    objName = "City." + city_id
    if objName in storage.all():
        storage.get(City, city_id).delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def postCity(state_id=None):
    """Defines post method"""

    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    if storage.get(State, state_id) is None:
        abort(404)
    request.get_json()['state_id'] = state_id
    newCity = City(**request.get_json())
    newCity.save()
    return (jsonify(newCity.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def putCity(city_id):
    """Defines put method"""

    if not request.get_json():
        abort(400, 'Not a JSON')
    objName = "City." + city_id
    if (objName in storage.all()):
        newCity = storage.get(City, city_id)
        changeCity = request.get_json()
        for key, value in changeCity.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(newCity, key, value)
        newCity.save()
        return (jsonify(newCity.to_dict()), 200)
    else:
        abort(404)
