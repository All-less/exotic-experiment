import subprocess as sp
import re
import exotic


def connect_fpga():
    res = sp.check_output('djtgcfg', shell=True)
    if not res.startswith('ERROR: no command specified'):
        print "The output of command 'djtgcfg' is unexpected. " \
              "Please check whether it is correctly installed or contact" \
              "the system administrator."

    res = sp.check_output('djtgcfg enum | grep "Device: ' + exotic.CABLE_NAME + '"', shell=True)
    if len(res) < 1:
        print "The download cable cannot be detected." \
              "Please contact the system administrator for help."

    res = sp.check_output('djtgcfg init -d ' + exotic.CABLE_NAME + ' | grep ' + exotic.FPGA_NUMBER, shell=True)
    if len(res) < 1:
        print "The FPGA device cannot be detected." \
              "Please contact the system administrator for help."

    index = re.match(r'\s*Device (\d+): ' + exotic.FPGA_NUMBER, res).groups()[0]
    return index


