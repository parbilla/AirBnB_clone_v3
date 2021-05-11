#!/usr/bin/python3
"""New view for the link between Place objects and Amenity objects
 that handles all default RestFul API actions"""
import os
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def getAmenity(place_id=None):
    """Defines get method"""
    if (("Place." + place_id) in storage.all()):
        amenitiesList = []
        objPlace = storage.get(Place, place_id)
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            place_amenities = objPlace.amenities
        else:
            place_amenities = objPlace.amenity_ids
        for amenity in place_amenities:
            amenitiesList.append(amenity.to_dict())
        return jsonify(amenitiesList)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delAmenity(place_id, amenity_id):
    """Defines delete method"""

    if (("Place." + place_id) in storage.all()):
        if (("Amenity." + amenity_id) in storage.all()):
            objPlace = storage.get(Place, place_id)
            objAmenity = storage.get(Amenity, amenity_id)
            if os.getenv('HBNB_TYPE_STORAGE') == 'db':
                place_amenities = objPlace.amenities
            else:
                place_amenities = objPlace.amenity_ids
            if objAmenity in place_amenities:
                place_amenities.remove(objAmenity)
                objPlace.save()
                return (jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def posAmenity(place_id, amenity_id):
    """Defines post method"""

    objPlace = storage.get(Place, place_id)
    objAmenity = storage.get(Amenity, amenity_id)
    if objPlace is None or objAmenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = objPlace.amenities
    else:
        place_amenities = objPlace.amenity_ids
    if objAmenity in place_amenities:
        return (jsonify(objAmenity.to_dict()), 200)
    else:
        return (jsonify(objAmenity.to_dict()), 201)
