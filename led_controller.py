import socket
import logging
import threading
from flask import Flask
import pigpio

udp_port=9999
pin_red=23
pin_green=25
pin_blue=24
logging.basicConfig(filename='led_controller.log',level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
pi=pigpio.pi()

app = Flask(__name__)

#execute pigpiod

#split to files
#	stream
#	database handle
#	color api (set colors)


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
		r=int(str_color[0:2],16)
		g=int(str_color[2:4],16)
		b=int(str_color[4:6],16)
		setcolor(r,g,b)
	return 1
	
	
	
	
	
#listens on udp port for colors to set in realtime
@app.route("/stream")
def stream():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#send exit command to stream mode so it exits if it is running before
	s.sendto('exit'.encode(), ("127.0.0.1", udp_port))
	threading.Thread(target=streamthread).start()	
	return "success"


	

	
#sets color from requested ressource
#sets flag to wait mode and sends udp packet to socket
# => stream mode terminates if running 		
@app.route("/colorhex/<hexcode>")
def colorhex(hexcode):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto('exit'.encode(), ("127.0.0.1", udp_port))
	#parse hexstring to colors as integer values
	r=int(hexcode[0:2],16)
	g=int(hexcode[2:4],16)
	b=int(hexcode[4:6],16)
	return setcolor(r,g,b)

	

	
	
	
#set gpio values according to rgb-color 	
def setcolor(red,green,blue):
	msg= 'r={0}, g={1}, b={2}'.format(red,green,blue)
	pi.set_PWM_dutycycle(pin_red,red)
	pi.set_PWM_dutycycle(pin_green,green)
	pi.set_PWM_dutycycle(pin_blue,blue)
	return msg
	
	
	
	
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=udp_port)	
			
