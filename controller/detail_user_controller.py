from flask import jsonify, request
import json
from model.user import *

def singleTransform(details):
    data = {
        'address': details.address,
        'phone_number': details.phone_number,
        'email': details.email,
    }
    return data