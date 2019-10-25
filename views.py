import logging
import socket

from util import hex2rgb,config
from pin_controller import setcolorbyhex,streamthread
from led_controller import app

log = logging.getLogger(__name__)

#listens on udp port for colors to set in realtime
#sends udp packet to localhost socket => stream mode restarts if running 	
@app.route("/stream")
def stream():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#send exit command to stream mode so it exits if it is running before
	s.sendto('exit'.encode(), ("127.0.0.1", udp_port))
	threading.Thread(target=streamthread).start()	
	return "success"

	
#sets color from requested ressource
#sends udp packet to localhost socket => stream mode terminates if running 		
@app.route("/colorhex/<hexcode>")
def colorhex(hexcode):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#send exit command to stream mode so it exits if it is running before
	s.sendto('exit'.encode(), ("127.0.0.1", config['udp_port']))
	#parse hexstring to colors as integer values
	return setcolorbyhex(hexcode)

	