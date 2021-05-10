#!/usr/bin/python3
"""New view for the link between Place objects and Amenity objects
 that handles all default RestFul API actions"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from models.user import User


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def getAmenity(place_id=None):
    """Defines get method"""
    if (("Place." + place_id) in storage.all()):
        amenities = []
        for amenity in storage.all("Amenity").values():
            if (amenity.place_id == place_id):
                amenities.append(amenity.to_dict())
        return jsonify(amenities)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delAmenity(place_id, amenity_id):
    """Defines delete method"""

    objPlace = "Place." + place_id
    if (objPlace in storage.all()):
        objName = "Amenity." + amenity_id
        if objName in storage.all():
            if objName in objPlace.amenities:
                storage.get(Amenity, amenity_id).delete()
                storage.save()
                return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def posAmenity(place_id, amenity_id):
    """Defines post method"""

    if storage.get(Place, place_id) is None:
        abort(404)
    if storage.get(Amenity, amenity_id) is None:
        abort(404)
    print(storage.get(Place, place_id))
    print(storage.get(Amenity, amenity_id))
    if storage.get(Amenity, amenity_id) in storage(Place, place_id).amenities:
        return jsonify(storage.get(Amenity, amenity_id).to_dict), 200
    else:
        return jsonify(storage.get(Amenity, amenity_id).to_dict), 201
