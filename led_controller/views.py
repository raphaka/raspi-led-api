import logging
import socket
import threading
from flask import request, jsonify

from led_controller.util import hex_2_rgb,Glob
from led_controller.pin_controller import set_color_by_hex,stream_thread
from led_controller.models import Color, ColorSchema
from led_controller import app,db

log = logging.getLogger(__name__)


#listens on udp port for colors to set in realtime
#sends udp packet to localhost socket => stream mode restarts if running 
#TODO Error handling
@app.route('/set/stream')
def stream():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #send exit command to stream mode so it exits if it is running before
    s.sendto('exit'.encode(), ("127.0.0.1", Glob.config['udp_port']))
    log.debug('Sent "exit" signal to stream mode udp port on localhost')
    threading.Thread(target=stream_thread).start()
    log.info('Started new thread for stream mode')
    return "success"


#sets color from requested ressource
#sends udp packet to localhost socket => stream mode terminates if running 
#TODO Error handling
@app.route('/set/colorhex/<hexcode>')
def colorhex(hexcode):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #send exit command to stream mode so it exits if it is running before
    s.sendto('exit'.encode(), ("127.0.0.1", Glob.config['udp_port']))
    log.debug('Sent "exit" signal to stream mode udp port on localhost')
    log.info('Setting color ' + hexcode)
    return set_color_by_hex(hexcode)


#GET: return array of colors
#POST: Add new color
@app.route('/colors', methods = ['GET', 'POST', 'DELETE'])
def list_fav_colors():
    #add new color
    if request.method == 'POST':
        #check content type and json syntax
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)
        data = request.get_json()
        item_name = data.get('name')
        item_value = data.get('value')
        if not item_name or not item_value:
            return response('failed', 'Name or value attribute not found', 400)
        #insert new record in database
        try: #TODO update if existing
            db.session.add(Color(name=item_name, value=item_value))
            db.session.commit()
        except:
            log.error('Could not insert new color into database')
            return 'fail' 
        return 'success'
    #delete color
    if request.method == 'DELETE':
        #check content type and json syntax
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)
        data=request.get_json()
        item_name = data.get('name')
        item_id = data.get('id')
        if not item_name and not item_id:
            return response('failed', 'No name or id attribute found', 400)
        #delete record from database
        try: #TODO: error message when not found in db
            if item_id:
                c = db.session.query(Color).get(item_id)
            elif item_name:
                c = db.session.query(Color).get(item_name)
            db.session.delete(c)
            db.session.commit()
        except:
            log.error('Could not delete color from database')
            return 'failed' 
        return "success"
    #list existing colors
    else:
        dictc = {}
        recs=db.session.query(Color).all()
        #Convert Records class from Color to dictionaries
        dictc['colors'] = ColorSchema(many=True).dump(recs) 
        return jsonify(dictc)
