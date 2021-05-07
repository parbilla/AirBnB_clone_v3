#!/usr/bin/python3
"""Create index"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify


@app_views.route('/status')
def status_url():
    """Method that returns a status JSON"""
    return jsonify({"status": "OK"})
