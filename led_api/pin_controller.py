import logging
import socket
import pigpio
import time
from datetime import datetime

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
    try:
        r,g,b = hex_2_rgb(colorhex)
    except ValueError:
        return "failed: no valid hexadecimal color value"
    return set_color(r,g,b)

#set gpio values according to rgb-color
#output value is calculated using a power function and the contrast_adjustment value in the config
#the power function always cuts 1:1 and the pitch increases as the input value gets higher
#the coordinate 1:1 is set to the brightness_maximum by multiplication/division
def set_color(red,green,blue):
    global pi
    c = Glob.config['contrast_adjustment']
    m = Glob.config['brightness_maximum']
    red = ((red/255) ** c)*m
    blue = ((blue/255) ** c)*m
    green = ((green/255) ** c)*m
    msg= 'setting output to:   r={0}, g={1}, b={2}'.format(red,green,blue)
    if Glob.config['pins_enabled']:
        pi.set_PWM_dutycycle(Glob.config['pin_red'],red)
        pi.set_PWM_dutycycle(Glob.config['pin_green'],green)
        pi.set_PWM_dutycycle(Glob.config['pin_blue'],blue)
    else:
        print(msg)
    return msg

#fades to color
def fade_to_color(start_color, target_color, duration): #duration in ms
    fade_start = datetime.now()
    period = 1000/Glob.config['fade_frequency']
    print(period)
    r,g,b = hex_2_rgb(start_color)
    end_r,end_g,end_b = hex_2_rgb(target_color)
    num_steps = int(duration / period)
    if num_steps > 0:  #only execute if theres at least one step in fade progress
        step_r = (end_r-r)/num_steps
        step_g = (end_g-g)/num_steps
        step_b = (end_b-b)/num_steps
        periodseconds = period/1000 #saved to value, so this division is not performed every loop
        for x in range(0, num_steps):
            time_start = datetime.now()
            r = r + step_r
            g = g + step_g
            b = b + step_b
            set_color(r,g,b)
            exec_time = datetime.now() - time_start
            if (periodseconds > exec_time.total_seconds()):
                time.sleep(periodseconds - exec_time.total_seconds()) #TODO MUST BE >=0 (frequency can be set by user)
    time.sleep((duration % period)/1000) #correction if period is not a whole multiple of duration
    set_color_by_hex(target_color)
    actual_duration = datetime.now() - fade_start
    return('finished: r=' + str(int(r)) + ' g=' + str(int(g)) + ' b=' + str(int(b))  + ' time=' + str(actual_duration))
