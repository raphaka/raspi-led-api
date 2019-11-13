import logging
import socket
import threading

from led_api.util import Glob
from led_api.pin_controller import set_color_by_hex
from led_api import app,db
log = logging.getLogger(__name__)

#listens on udp port for colors to set in realtime
#sends udp packet to localhost socket => stream mode restarts if running 
@app.route('/set/stream')
def stream():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #send exit command to stream mode so it exits if it is running before
        s.sendto('exit'.encode(), ("127.0.0.1", Glob.config['udp_port']))
        log.debug('Sent "exit" signal to stream mode udp port on localhost')
        threading.Thread(target=stream_thread).start()
        log.info('Started new thread for stream mode')
    except:
        log.error('could not start stream mode')
        return "failure: could not start stream mode"
    return "success"


#sets color from requested ressource
#sends udp packet to localhost socket => stream mode terminates if running 
@app.route('/set/colorhex/<hexcode>')
def colorhex(hexcode):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #send exit command to stream mode so it exits if it is running before
        s.sendto('exit'.encode(), ("127.0.0.1", Glob.config['udp_port']))
        log.debug('Sent "exit" signal to stream mode udp port on localhost')
        log.info('Setting color ' + hexcode)
    except:
        log.error('Could not set color')
        return "failure: could not set color"
    return set_color_by_hex(hexcode)