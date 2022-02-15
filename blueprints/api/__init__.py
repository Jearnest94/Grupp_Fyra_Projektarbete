import json
import os
from flask import Blueprint, request, Response
from controllers import user_controller

bp_api = Blueprint('bp_api', __name__)


@bp_api.get('/users')
def get_server_ip():
    pass
