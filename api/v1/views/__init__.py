#!/usr/bin/python3
"""Initialize Blueprint"""
from flask import Blueprint


app_views = Blueprint("app_views", 'name', url_prefix="/api/v1")

from api.v1.views.index import *
