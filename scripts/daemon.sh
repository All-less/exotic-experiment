#!/bin/bash

set -e

if [ "$(whoami)" != "root" ]; then
    echo "Error! Root privilege required for this script."
    exit 1
fi 

# the absolute path to the jupyter notebook daemon
# change this path based on your system configuration
DAEMON=/var/www/exotic-rpi/env/bin/python

# the name of the process
NAME=EXOTIC_RPI

# options to pass to the daemon
# this assumes that all the options are already configured
# in the configuration file
DAEMON_OPTS='/var/www/exotic-rpi/main.py --config=/var/www/exotic-rpi/config.py'

# options to pass to start-stop-daemon
INIT_OPTS='--quiet --background --chuid=root --chdir=/var/www/exotic-rpi'

# options to redirect output
REDIR_OPTS='1>>/var/log/exotic-rpi/stdout.log 2>>/var/log/exotic-rpi/stderr.log'

# the process file that will be used by this script
# this will be used for the start and the stop commands
# by default, this will be created in the directory where
# this file is residing
PIDFILE=$NAME.pid

# process description
DESC="RPi Daemon for Exotic Experiment"

# the user that will be used to run the daemon
# you can change this to a different user if you want
RUNAS=root

# check if the program is running or not
test -x $DAEMON || exit 0

case "$1" in
  start)
    # start the daemon
    start-stop-daemon --start --quiet --pidfile "$PIDFILE" --exec "$DAEMON" --test > /dev/null
    # here we use eval to make redirection take effect
    eval "start-stop-daemon $REDIR_OPTS --start --make-pidfile --pidfile $PIDFILE $INIT_OPTS --exec $DAEMON -- $DAEMON_OPTS"
    ;;
  stop)
    # stop the process
    start-stop-daemon --stop --pidfile $PIDFILE
    rm -f $PIDFILE

    ;;
  reload|force-reload|restart)
    # check if the process can be killed
    if start-stop-daemon --stop --pidfile $PIDFILE; then
        # if the process was killed, start it again
        start-stop-daemon --start --quiet --pidfile "$PIDFILE" --exec "$DAEMON" --test > /dev/null
        eval "start-stop-daemon $REDIR_OPTS --start --make-pidfile --pidfile $PIDFILE $INIT_OPTS --exec $DAEMON -- $DAEMON_OPTS"
    fi
    ;;
  status)
    echo -n "Status of $DESC: "
    
    # check if the file is existing or not
    if [ ! -r "$PIDFILE" ]; then
        # if the file does not exist, it is not running
        echo "$NAME is not running."
        exit 3
    fi

    # check if the file is existing and get the process id
    # read the process id number from the file
    if read pid < "$PIDFILE" && ps -p "$pid" > /dev/null 2>&1; then
        # if the process id exists, then it is running
        echo "$NAME is running."
        exit 0
    else
        # otherwise, the process file is still there but the
        # daemon is not running anymore
        echo "$NAME is not running but $PIDFILE exists."
        exit 1
    fi
    ;;
  *)
    N=${0##*/}
    # default case
    echo "Usage: $N {start|stop|restart|force-reload|status}" >&2
    exit 1
esac

exit 0
