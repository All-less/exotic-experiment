import subprocess as sp
import re
import exotic as ex
import logging


def connect_fpga():
    try:
        res = sp.check_output('djtgcfg', shell=True)
    except sp.CalledProcessError as e:
        res = e.output
    if not res.startswith('ERROR: no command specified'):
        logging.error("The output of command 'djtgcfg' is unexpected. " +
                      "Please check whether it is correctly installed.")
        ex.exit(1)
        

    try:
        res = sp.check_output('djtgcfg enum | grep "Device: ' + ex.CABLE_NAME + '"', shell=True)
        if len(res) < 1:
            logging.error("The download cable cannot be detected.")
            ex.exit(1)

        res = sp.check_output('djtgcfg init -d ' + ex.CABLE_NAME + ' | grep ' + ex.FPGA_NUMBER, shell=True)
        if len(res) < 1:
            logging.error("The FPGA device cannot be detected.")
            ex.exit(1)
    except Exception as e:
        logging.error("Some unexpected error occurs during connecting to FPGA. Below is error info.")
        logging.error(str(e))
        ex.exit(1)

    index = re.match(r'\s*Device (\d+): ' + ex.FPGA_NUMBER, res).groups()[0]
    logging.info('Successfully connect to the FPGA board.')
    return index


def program_fpga(file_path):
    index = connect_fpga()
    try:
        res = sp.check_output('file ' + file_path, shell=True)

        res = sp.check_output('djtgcfg prog -d ' + ex.CABLE_NAME + ' --index ' + str(index) +
                              ' --file ' + file_path + '| grep "Programming succeeded."', shell=True)
        if len(res) < 1:
            logging.error("Some unexpected error occurs during programming the FPGA board.")
            ex.exit(1)
        else:
            logging.info("Programming " + file_path + " to FPGA succeeded!")
    except Exception as e:
        logging.error("Some unexpected error occurs during programming the FPGA board. Below is error info.")
        logging.error(str(e))
        ex.exit(1)
