from config.config import app,Resource, bcrypt,create_access_token
from flask import session, request, redirect

class Index_controller(Resource):
    def __init__(self):
        pass
    def get(self):
        return 'Hello World'