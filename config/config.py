from flask import Flask,session
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask.logging import default_handler

import configparser
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import os
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

config = configparser.ConfigParser()
config.read('.env')
configurate = config['CONFIGURATION']

app = Flask(__name__,template_folder=os.getcwd()+'/resource/view/',static_folder=os.getcwd()+'/public/',static_url_path='')
app.logger.removeHandler(default_handler)

app.config['SECRET_KEY'] = configurate.get('APP_KEY')
if configurate.get('APP_DEBUG') == 'false':
    app_debug = False
elif configurate.get('APP_DEBUG') == 'true':
    app_debug = True
app.debug = app_debug

app.config['SECRET_KEY'] = "AqWwxV*.xK3:'3EY)+@F>#/FT/\}pcx}"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://'+configurate.get('DB_USERNAME')+':'+configurate.get('DB_PASSWORD')+'@'+configurate.get('DB_HOST')+'/'+configurate.get('DB_DATABASE')
SQLALCHEMY_TRACK_MODIFICATIONS = False
bcrypt = Bcrypt(app)
 
db = SQLAlchemy(app)

db.init_app(app)

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*","headers":"X-Custom-Header"}})

