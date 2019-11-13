import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from led_api.util import Glob,read_json
from led_api.pin_controller import start_pigpio

app = Flask(__name__)
app.config.from_pyfile('flask_config.cfg')
db = SQLAlchemy(app)
ma = Marshmallow(app)   #Wrapper to make SQLalchemy objects JSON Serializable
from led_api.views import colors,setpins,settings

Glob.config = read_json('config.json')
logging.basicConfig(filename=Glob.config['log_file'],level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
start_pigpio()
db.create_all()