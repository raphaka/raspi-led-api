import json

#TODO Error Handling
def read_json(input):
        with open(input, 'r') as infile:
                return json.loads(infile.read())

def hex_2_rgb(str_colorhex):
        r=int(str_colorhex[0:2],16)
        g=int(str_colorhex[2:4],16)
        b=int(str_colorhex[4:6],16)
        return r,g,b

class Glob(object):
        config = {}