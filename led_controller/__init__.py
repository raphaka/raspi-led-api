import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from led_controller.util import Glob,read_json

app = Flask(__name__)
app.config.from_pyfile('flask_config.cfg')
db = SQLAlchemy(app)
from led_controller import views

Glob.config = read_json('config.json')
logging.basicConfig(filename=Glob.config['log_file'],level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
db.create_all()