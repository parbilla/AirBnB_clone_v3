#!/usr/bin/python3
"""New view for User objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def getUser(user_id=None):
    """Defines get method"""

    if (user_id):
        objName = "User." + user_id
        if (objName in storage.all()):
            return jsonify((storage.get(User, user_id)).to_dict())
        else:
            abort(404)
    else:
        users = []
        for user in storage.all("User").values():
            users.append(user.to_dict())
        return jsonify(users)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteUser(user_id):
    """Defines delete method"""

    objName = "User." + user_id
    if objName in storage.all():
        storage.get(User, user_id).delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def postUser():
    """Defines post method"""

    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    newUser = User(**request.get_json())
    newUser.save()
    return (jsonify(newUser.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def putUser(user_id):
    """Defines put method"""

    if not request.get_json():
        abort(400, 'Not a JSON')
    objName = "User." + user_id
    if (objName in storage.all()):
        newUser = storage.get(User, user_id)
        changeUser = request.get_json()
        for key, value in changeUser.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(newUser, key, value)
        newUser.save()
        return (jsonify(newUser.to_dict()), 200)
    else:
        abort(404)
