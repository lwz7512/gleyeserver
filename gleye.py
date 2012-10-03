# -*- coding: utf-8 *-*
"""
This is a starter app for a series of monitoring products, aiming to realtime
check the server/database/business running status, first use ubuntu to test!

    2012/09/19 by lwz7512

"""
# Libraries
#==========

import sys
import time

# Test methods
#=============

try:
    import psutil
except ImportError:
    print('PsUtil module not found. Glances cannot start.')
    print()
    print('On Ubuntu 12.04 or higher:')
    print('$ sudo apt-get install python-psutil')
    print()
    print('To install PsUtil using pip (as root):')
    print('# pip install psutil')
    print()
    sys.exit(1)
else:
    print('pstuil is ready...')
# to test more...

counter = None    # this is a global var declaration...


def init():
    global counter    # use global to reference it
    counter = 1    # initialize it
    print 'start opening eye...'


def poll_cpu_num():
    cpu_num = psutil.NUM_CPUS

    return cpu_num


def poll_total_cpu():
    # non-blocking (percentage since last call)
    cpu_usage = psutil.cpu_percent(interval=0)

    return cpu_usage


def poll_per_cpu():
    # non-blocking (percentage since last call)
    cpu_usage = psutil.cpu_percent(interval=0, True)

    return cpu_usage


def poll_process_info():
    pass    # TODO, ...


def main():
    global counter    # reference it before use in a function
    # Init stuff
    init()
    # this interval is ideal, cpu usage for this script drop to <= 2.0%
    interval = 3    # seconds
    cpu = 'total cpu usage: '
    # Main loop
    try:
        while True:
            args = poll_total_cpu()    # poll cpu usage...
            print_msg(cpu + str(args))    # show...
            # sleep some time
            time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        print 'program exited...'
        pass


def print_num(value):
    print str(value)


def print_msg(msg):
    print msg


def end():
    sys.exit(0)


# Main
#=====

if __name__ == "__main__":
    main()

# The end...
