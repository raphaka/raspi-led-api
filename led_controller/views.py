import logging
import socket
import threading
from flask import request

from led_controller.util import hex_2_rgb,Glob
from led_controller.pin_controller import set_color_by_hex,stream_thread
from led_controller.models import Color
from led_controller import app,db

log = logging.getLogger(__name__)


#listens on udp port for colors to set in realtime
#sends udp packet to localhost socket => stream mode restarts if running 
@app.route('/set/stream')
def stream():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #send exit command to stream mode so it exits if it is running before
    s.sendto('exit'.encode(), ("127.0.0.1", Glob.config['udp_port']))
    log.debug('Sent "exit" signal to stream mode udp port on localhost')
    threading.Thread(target=stream_thread).start()
    log.info('Started new thread for stream mode')
    return "success"


#TODO: rename
#sets color from requested ressource
#sends udp packet to localhost socket => stream mode terminates if running 
@app.route('/set/colorhex/<hexcode>')
def colorhex(hexcode):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #send exit command to stream mode so it exits if it is running before
    s.sendto('exit'.encode(), ("127.0.0.1", Glob.config['udp_port']))
    log.debug('Sent "exit" signal to stream mode udp port on localhost')
    log.info('Setting color ' + hexcode)
    return set_color_by_hex(hexcode)


#GET: return array of colors
#POST: Add new color
#DELETE: TODO
@app.route('/colors', methods = ['GET', 'POST'])
def list_fav_colors():
    #add new color
    if request.method == 'POST':
        data=request.get_json()
        try: #TODO update if existing
            db.session.add(Color(name=data['name'], value=data['value']))
            db.session.commit()
        except:
            log.error('Could not insert new color into database')
            return 'fail' 
        return 'success'
    #list existing colors
    else:
        colors = Color.query.all()
        return colors
