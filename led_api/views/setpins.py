import logging
import socket
import threading
from flask import request

from led_api.util import Glob
from led_api.pin_controller import set_color_by_hex, fade_to_color
from led_api.threads import stream_thread,effect_thread
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

# starts effect sent in body
@app.route('/set/effect', methods = ['POST'])
def res_testeffect():
    try:
        if not request.content_type == 'application/json':
            return ('failed: Content-type must be application/json', 401)
        data = request.get_json()
        #stop old thread if running
        Glob.thread_stop = True
        if Glob.current_thread.is_alive():
            Glob.current_thread.join()
        #create a new thread
        item_effect = data.get('effect')
        if not item_effect:
            return ('failed: Effect attribute not found', 400)
        Glob.current_thread = threading.Thread(target=effect_thread, args=(item_effect,))
        Glob.current_thread.start()
    except:
        log.error('could not start effect mode')
        return ('failure: Could not start effect mode', 500)
        print(Glob.current_thread)
    if Glob.thread_stop == False and Glob.current_thread.is_alive():
        log.info('Started new thread for effect mode')
        return 'success'
    else:
        logging.error('effect thread could not be started due to an error.')
        return ('could not start this effect. Please check the syntax.', 400)
