# -*- coding: utf-8 *-*
"""
This is a starter app for a series of monitoring products, aiming to realtime
check the server/database/business running status, first use ubuntu to test!

    2012/09/19 by lwz7512

"""
# Libraries
#==========
import cherrypy
import collecttask
import os.path


tutconf = os.path.join(os.path.dirname(__file__), 'server.conf')


class HelloWorld:

    def index(self):
        start()
        return "<a href='stopCollect'>Click to stop</a>"
    index.exposed = True

    def stopCollect(self):
        stop()
        return "Stoped!  <a href='../'>click to start</a>"
    stopCollect.exposed = True


def start():
    collecttask.go()


def stop():
    collecttask.stop()


def status():
    return collecttask.isRunning()


def main():
    cherrypy.quickstart(HelloWorld(), config=tutconf)


# Main
#=====

if __name__ == "__main__":
    main()

# The end...
