# -*- coding: utf-8 *-*
"""
This is a starter app for a series of monitoring products, aiming to realtime
check the server/database/business running status, first use ubuntu to test!

    2012/09/19 by lwz7512

"""
# Libraries
#==========

import collecttask


def main():
    collecttask.main()


def stop():
    collecttask.stop()


def status():
    return collecttask.isRunning()

# Main
#=====

if __name__ == "__main__":
    main()

# The end...
