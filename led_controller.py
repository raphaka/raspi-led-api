import logging
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('flask_config.cfg')
from views import *

if __name__ == "__main__":
	logging.basicConfig(filename='led_controller.log',level=logging.DEBUG,
	format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
	app.run()	
			

#TODO
#check if sending exit to localhost still works for stopping stream mode


#todo
#add settings page
#add effect (list of dict) number, name, json
#[
#	{'color':'00ff00', 'duration':500, 'fade':True},
#	{''}
#]
#add to effect (update json in db)
#delete effect
#delete from effect
#add fav color (number, name, hex)
#remove fav color