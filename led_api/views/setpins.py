import logging
import socket
import threading

from led_api.util import Glob
from led_api.pin_controller import set_color_by_hex, stream_thread
from led_api import app,db
log = logging.getLogger(__name__)

#listens on udp port for colors to set in realtime
#sends udp packet to localhost socket => stream mode restarts if running
@app.route('/set/stream')
def res_stream():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #send exit command to stream mode so it exits if it is running before
        s.sendto('exit'.encode(), ("127.0.0.1", Glob.config['udp_port']))
        log.debug('Sent "exit" signal to stream mode udp port on localhost')
        threading.Thread(target=stream_thread).start()
        log.info('Started new thread for stream mode')
    except:
        log.error('could not start stream mode')
        return ("failure: Could not start stream mode", 500)
    return "success"


#sets color from requested ressource
#sends udp packet to localhost socket => stream mode terminates if running
@app.route('/set/colorhex/<hexcode>')
def res_colorhex(hexcode):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #send exit command to stream mode so it exits if it is running before
        s.sendto('exit'.encode(), ("127.0.0.1", Glob.config['udp_port']))
        log.debug('Sent "exit" signal to stream mode udp port on localhost')
        log.info('Setting color ' + hexcode)
    except:
        log.error('Could not set color')
        return ("failure: could not set color", 500)
    msg = set_color_by_hex(hexcode)
    if ('failed' in msg):
        return (msg,400)
    return msg
