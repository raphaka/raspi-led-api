import logging
import socket
import pigpio

from led_api.util import hex_2_rgb, Glob
log = logging.getLogger(__name__)

global pi

def start_pigpio():
    global pi
    if Glob.config['pins_enabled']:
        pi=pigpio.pi()

#start stream mode on UDP port and change color in realtime
def stream_thread():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", Glob.config['udp_port']))
        log.info ("Stream mode waiting on port:"+ str(Glob.config['udp_port']))
    except:
        log.error('could not start stream thread on udp port')
        return 1
    while 1:
        str_color, addr = s.recvfrom(1024)
        str_color = str_color.decode()
        if (str_color == 'exit'):
            return 1
        log.debug("parsing string: " + str(str_color))
        set_color_by_hex(str_color)
    return 1

#set gpio values according to rgb-color-hex
def set_color_by_hex(colorhex):
    r,g,b = hex_2_rgb(colorhex)
    return set_color(r,g,b)

#set gpio values according to rgb-color
#output value is calculated using a power function and the contrast_boost value in the config 
def set_color(red,green,blue):
    global pi
    msg= 'received rgb values:   r={0}, g={1}, b={2}'.format(red,green,blue)
    c = Glob.config['contrast_adjustment']
    red = ((red/255) ** c)*255
    blue = ((blue/255) ** c)*255
    green = ((green/255) ** c)*255
    msg= 'setting output to:   r={0}, g={1}, b={2}'.format(red,green,blue)
    if Glob.config['pins_enabled']:
        pi.set_PWM_dutycycle(Glob.config['pin_red'],red)
        pi.set_PWM_dutycycle(Glob.config['pin_green'],green)
        pi.set_PWM_dutycycle(Glob.config['pin_blue'],blue)
    else:
        print(msg)
    return msg
