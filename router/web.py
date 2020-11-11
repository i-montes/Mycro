from config.config import api,app
from app.Http.controller.index_controller import Index_controller 

api.add_resource(Index_controller, '/')
