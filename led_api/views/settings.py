import logging
from flask import request, jsonify

from led_api.util import Glob, write_config
from led_api import app

log = logging.getLogger(__name__)

#retrieve new config
#or update the sent values on server side
@app.route('/settings', methods = ['GET', 'PUT'])
def res_settings():
    if request.method == 'PUT':
        if not request.content_type == 'application/json':
            return ('failed: Content type must be application/json', 401)
        data = request.get_json()
        for k in data:
            if k in Glob.config.keys():
                Glob.config[k] = data[k]
        if write_config() == 0:
            log.info('updated config file')
            return 'success'
        else:
            return('failed: Could not write settings to output file', 500)
    else:
        return jsonify(Glob.config)