import subprocess as sp
import exotic
import os


process = None


def rpi_init():
    for pin in exotic.RPI_INPUTS:
        sp.check_output('gpio mode ' + str(pin) + ' in', shell=True);
        sp.check_output('gpio mode ' + str(pin) + ' up', shell=True);
    for pin in exotic.RPI_OUTPUTS:
        sp.check_output('gpio mode ' + str(pin) + ' out', shell=True);


def rpi_write(pin, val):
    sp.check_output('gpio write ' + str(pin) + ' ' + str(val), shell=True);


def start_streaming():
    process = sp.Popen(
        "raspivid -t 0 -w 960 -h 540 -fps 25 -b 500000 -vf -hf -o - | " + 
        "ffmpeg -i - -vcodec copy -an -r 25 -f flv -metadata streamName=test tcp://10.214.128.116:6666",
        stdout=sp.PIPE, shell=True, preexec_fn=os.setsid)


def stop_streaming():
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

