import subprocess as sp
import re
import exotic as ex
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
        ex.exit(1)
        

    try:
        res = sp.check_output('djtgcfg enum | grep "Device: ' + ex.CABLE_NAME + '"', shell=True)
        if len(res) < 1:
            print "The download cable cannot be detected.\n" \
                  "Please contact the system administrator for help."
            ex.exit(1)

        res = sp.check_output('djtgcfg init -d ' + ex.CABLE_NAME + ' | grep ' + ex.FPGA_NUMBER, shell=True)
        if len(res) < 1:
            print "The FPGA device cannot be detected.\n" \
                  "Please contact the system administrator for help."
            ex.exit(1)
    except:
        print "Some unexpected error occurs during connection to FPGA.\n" \
              "Please contact the system administrator for help."
        ex.exit(1)

    index = re.match(r'\s*Device (\d+): ' + ex.FPGA_NUMBER, res).groups()[0]
    return index


def program_fpga(file_path):
    index = connect_fpga()
    try:
        res = sp.check_output('file ' + file_path, shell=True)

        res = sp.check_output('djtgcfg prog -d ' + ex.CABLE_NAME + ' --index ' + str(index) +
                              ' --file ' + file_path + '| grep "Programming succeeded."', shell=True)
        if len(res) < 1:
            print "Some unexpected error occurs during programming the FPGA board.\n" \
                  "Please contact the system administrator for help."
            ex.exit(1)
        else:
            print "Programming " + file_path + " to FPGA succeeded!"
    except:
        print "Some unexpected error occurs during programming the FPGA board.\n" \
              "Please contact the system administrator for help."
        ex.exit(1)
