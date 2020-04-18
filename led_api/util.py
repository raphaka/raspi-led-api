import json
import sys
import logging

log = logging.getLogger(__name__)

def read_json(input):
    try:
        with open(input, 'r') as infile:
                return json.loads(infile.read())
    except:
        print('ERROR: Could not load config file')
        sys.exit()

def write_json(outpath, data):
    try:
        with open(outpath, 'w') as outfile:
            json.dump(data, outfile)
        return 0
    except:
        log.error('Could not write config file')
        sys.exit()

def write_config():
    return(write_json('config.json',Glob.config))

def hex_2_rgb(str_colorhex): #throws ValueError
        r=int(str_colorhex[0:2],16)
        g=int(str_colorhex[2:4],16)
        b=int(str_colorhex[4:6],16)
        return r,g,b

class Glob(object):
        config = {}
