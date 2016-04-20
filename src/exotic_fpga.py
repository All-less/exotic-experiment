import subprocess as sp
import re
import exotic
import sys


def connect_fpga():
    try:
        res = sp.check_output('djtgcfg', shell=True)
    except sp.CalledProcessError as e:
        res = e.output
    if not res.startswith('ERROR: no command specified'):
        print "The output of command 'djtgcfg' is unexpected. \n" \
              "Please check whether it is correctly installed or contact\n" \
              "the system administrator."
        sys.exit(0)

    try:
        res = sp.check_output('djtgcfg enum | grep "Device: ' + exotic.CABLE_NAME + '"', shell=True)
        if len(res) < 1:
            print "The download cable cannot be detected.\n" \
                  "Please contact the system administrator for help."
            sys.exit(0)

        res = sp.check_output('djtgcfg init -d ' + exotic.CABLE_NAME + ' | grep ' + exotic.FPGA_NUMBER, shell=True)
        if len(res) < 1:
            print "The FPGA device cannot be detected.\n" \
                  "Please contact the system administrator for help."
            sys.exit(0)
    except:
        print "Some unexpected error occurs during connection to FPGA.\n" \
              "Please contact the system administrator for help."
        sys.exit(0)

    index = re.match(r'\s*Device (\d+): ' + exotic.FPGA_NUMBER, res).groups()[0]
    return index


def program_fpga(file_name):
    index = connect_fpga()
    try:
        res = sp.check_output('djtgcfg -d ' + exotic.CABLE_NAME + ' --index ' + str(index) +
                              ' --file ' + file_name + '| grep "Programming succeeded."', shell=True)
        if len(res) < 1:
            print "Some unexpected error occurs during programming the FPGA board.\n" \
                  "Please contact the system administrator for help."
            sys.exit(0)
        else:
            print "Programming " + file_name + " to FPGA succeeded!"
    except:
        print "Some unexpected error occurs during programming the FPGA board.\n" \
              "Please contact the system administrator for help."
        sys.exit(0)
