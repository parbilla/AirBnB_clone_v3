#!/usr/bin/python3
"""New view for Review objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def getReview1(review_id=None):
    """Defines get method 1"""
    objName = "Review." + review_id
    if (objName in storage.all()):
        return jsonify((storage.get(Review, review_id)).to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getReview2(place_id=None):
    """Defines get method 2"""
    if (("Place." + place_id) in storage.all()):
        reviews = []
        for review in storage.all("Review").values():
            if (review.place_id == place_id):
                reviews.append(review.to_dict())
        return jsonify(reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReview(review_id):
    """Defines delete method"""

    objName = "Review." + review_id
    if objName in storage.all():
        storage.get(Review, review_id).delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def postReview(place_id=None):
    """Defines post method"""

    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    if storage.get(Place, place_id) is None:
        abort(404)
    if storage.get(User, request.get_json()['user_id']) is None:
        abort(404)
    request.get_json()['place_id'] = place_id
    newReview = Review(**request.get_json())
    newReview.save()
    return (jsonify(newReview.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def putReview(review_id):
    """Defines put method"""

    if not request.get_json():
        abort(400, 'Not a JSON')
    objName = "Review." + review_id
    if (objName in storage.all()):
        newReview = storage.get(Review, review_id)
        changeReview = request.get_json()
        for key, value in changeReview.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(newReview, key, value)
        newReview.save()
        return (jsonify(newReview.to_dict()), 200)
    else:
        abort(404)
