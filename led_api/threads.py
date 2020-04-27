import socket
import logging

from led_api.util import Glob
from led_api.pin_controller import set_color_by_hex
log = logging.getLogger(__name__)

#start stream mode on UDP port and change color in realtime
def stream_thread():
    Glob.thread_stop = False
    sock_timeout = Glob.config['socket_timeout']
    timeouts = 3
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", Glob.config['udp_port']))
        s.settimeout(sock_timeout)
        log.info ("Stream mode waiting on port:"+ str(Glob.config['udp_port']))
    except:
        log.error('could not start stream thread on udp port')
        return 1
    while 1:
        #stop if flag is set
        if (Glob.thread_stop == True):
            logging.info('Stream: Terminating - Stop flag has been set')
            return 1
        try:
            str_color, addr = s.recvfrom(1024)
            str_color = str_color.decode()
            log.debug("parsing string: " + str(str_color))
            set_color_by_hex(str_color)
        except socket.timeout:
            timeouts -= 1
            if timeouts == 0:
                logging.error("Stream thread timed out 3 times. Terminating")
                Glob.thread_stop = True
                return 1
            logging.info('Stream thread timed out after ' + str(sock_timeout) + ' seconds. Retrying...')
    return 1
