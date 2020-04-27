import logging
import socket
import threading
from flask import request

from led_api.util import Glob
from led_api.pin_controller import set_color_by_hex, fade_to_color
from led_api.threads import stream_thread
from led_api import app,db
log = logging.getLogger(__name__)

#listens on udp port for colors to set in realtime
#sends udp packet to localhost socket => stream mode restarts if running
@app.route('/set/stream')
def res_stream():
    try:
        #stop old thread if running
        Glob.thread_stop = True
        if Glob.current_thread.is_alive():
            Glob.current_thread.join()
        #create a new thread
        Glob.current_thread = threading.Thread(target=stream_thread)
        Glob.current_thread.start()
        log.info('Started new thread for stream mode')
    except:
        log.error('could not start stream mode')
        return ("failure: Could not start stream mode", 500)
    return "success"


#sets color from requested ressource
#sends udp packet to localhost socket => stream mode terminates if running
@app.route('/set/colorhex/<hexcode>')
def res_colorhex(hexcode):
    Glob.thread_stop = True
    log.info('Setting color ' + hexcode)
    msg = set_color_by_hex(hexcode)
    if ('failed' in msg):
        return (msg,400)
    return msg

#starts effect test
@app.route('/set/fade', methods = ['POST'])
def res_fade():
    if request.method == 'POST':
        Glob.thread_stop = True
        #check content type and json syntax
        if not request.content_type == 'application/json':
            return ('failed: Content-type must be application/json', 401)
        data = request.get_json()
        item_startcolor = data.get('startcolor')
        item_targetcolor = data.get('targetcolor')
        item_duration = data.get('duration') #TODO check if number
        if not item_startcolor or not item_targetcolor or not item_duration:
            return ('failed: startcolor, targetcolor or duration attribute not found', 400)
        #fade to color
        msg = fade_to_color(item_startcolor, item_targetcolor, item_duration)
        if ('failed' in msg):
            return (msg,400)
        return msg
