import logging
import threading
import socket
#import pigpio

from util import hex2rgb
log = logging.getLogger(__name__)

#pi=pigpio.pi()

def streamthread():
	logging.info("started stream mode thread in background")
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("", udp_port))
	print ("waiting on port:", udp_port)
	while 1:
		str_color, addr = s.recvfrom(1024)
		if (str_color == 'exit'):
			return 1
		logging.debug("parsing string: " + str_color)	
		#parse hexstring to colors as integer values
	setcolorbyhex(str_color)
	return 1
	
#set gpio values according to rgb-color 	
def setcolorbyhex(colorhex):
	r,g,b = hex2rgb(colorhex)
	return setcolor(r,g,b)

#set gpio values according to rgb-color 	
def setcolor(red,green,blue):
	msg= 'r={0}, g={1}, b={2}'.format(red,green,blue)
	#pi.set_PWM_dutycycle(pin_red,red)
	#pi.set_PWM_dutycycle(pin_green,green)
	#pi.set_PWM_dutycycle(pin_blue,blue)
	return msg
	
	