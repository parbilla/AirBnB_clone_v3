#!/usr/bin/python3
"""new view for State objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage

@app_views.route('/views/states', methods=['GET'])
@app_views.route('/views/states/<state_id>', methods=['GET'])

def getmethod(state_id=None):
    """get method def"""

    if (state_id):

        if ('state.' + state_id in storage.all()):
            return jsonify(storage.get(state, state_id).to_dict())
    else:
        return jsonify(storage.get(state).to_dict())