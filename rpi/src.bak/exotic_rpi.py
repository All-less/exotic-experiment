import subprocess as sp
import exotic as ex
import exotic_network as en
import os
import signal
import logging


def rpi_init():
    for pin in ex.RPI_INPUTS:
        sp.check_output('gpio mode ' + str(pin) + ' in', shell=True)
        sp.check_output('gpio mode ' + str(pin) + ' up', shell=True)
    for pin in ex.RPI_OUTPUTS:
        sp.check_output('gpio mode ' + str(pin) + ' out', shell=True)
    logging.info('GPIO ports initialization done.')


def rpi_write(pin, val):
    sp.check_output('gpio write ' + str(pin) + ' ' + str(val), shell=True)


def start_streaming():
    if not ex.process:
        ex.process = sp.Popen(
            "raspivid -t 0 -w 960 -h 540 -fps 25 -b 500000 -vf -hf -o - | " + 
            "ffmpeg -i - -vcodec copy -an -r 25 -f flv -metadata streamName=" + 
            en.status['stream_name'] + ' tcp://' + en.status['rtmp_host'] + ':' + 
            str(en.status['rtmp_port']) + " 1>/dev/null 2>/dev/null",
            stdout=sp.PIPE, shell=True, preexec_fn=os.setsid)
        logging.info('Start streaming to tcp://' + en.status['rtmp_host'] + ':' +
                     str(en.status['rtmp_port']))


def stop_streaming():
    if ex.process:
        os.killpg(os.getpgid(ex.process.pid), signal.SIGTERM)
        ex.process = None
        logging.info('Stop streaming.')

