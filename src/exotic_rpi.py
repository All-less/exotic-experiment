import subprocess as sp
import exotic


def rpi_init():
    for pin in exotic.RPI_INPUTS:
        sp.check_output('gpio mode ' + str(pin) + ' in', shell=True);
        sp.check_output('gpio mode ' + str(pin) + ' up', shell=True);
    for pin in exotic.RPI_OUTPUTS:
        sp.check_output('gpio mode ' + str(pin) + ' out', shell=True);


def rpi_write(pin, val):
    sp.check_output('gpio write ' + str(pin) + ' ' + str(val), shell=True);
