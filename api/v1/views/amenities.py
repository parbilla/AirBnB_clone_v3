#!/usr/bin/python3
"""New view for Amenities objects to handle all default RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getAmenities(amenity_id=None):
    """Defines get method"""

    if (amenity_id):
        objName = "Amenity." + amenity_id
        if (objName in storage.all()):
            return jsonify((storage.get(Amenity, amenity_id)).to_dict())
        else:
            abort(404)
    else:
        amenities = []
        for amenity in storage.all("Amenity").values():
            amenities.append(amenity.to_dict())
        return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """Defines delete method"""

    objName = "Amenity." + amenity_id
    if objName in storage.all():
        storage.get(Amenity, amenity_id).delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def postAmenity():
    """Defines post method"""

    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    newAmenity = Amenity(**request.get_json())
    newAmenity.save()
    return (jsonify(newAmenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def putAmenity(amenity_id):
    """Defines put method"""

    if not request.get_json():
        abort(400, 'Not a JSON')
    objName = "Amenity." + amenity_id
    if (objName in storage.all()):
        newAmenity = storage.get(Amenity, amenity_id)
        changeAmenity = request.get_json()
        for key, value in changeAmenity.items():
            if (key == 'name'):
                setattr(newAmenity, key, value)
        newAmenity.save()
        return (jsonify(newAmenity.to_dict()), 200)
    else:
        abort(404)
