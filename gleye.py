# -*- coding: utf-8 *-*
"""
This is a starter app for a series of monitoring products, aiming to realtime
check the server/database/business running status, first use ubuntu to test!

    2012/09/19 by lwz7512

"""
# Libraries
#==========
import ConfigParser
import json
import os.path
import socket

import showtable
import collecttask

localDir = os.path.dirname(__file__)
tutconf = os.path.join(localDir, 'server.conf')
cherrypy_available = None

try:
    import cherrypy
except ImportError:
    print 'cherrypy module not found. Gleye cannot start.'
    print ''
    print 'On Ubuntu 12.04 or higher:'
    print '$ sudo apt-get install python-cherrypy'
    print ''
    print 'or install cherrypy using pip (as root):'
    print '# pip install cherrypy'
    print ''
    cherrypy_available = False
else:
    print 'cherrypy  is ready to run...'
    cherrypy_available = True


class CollectData:

    def index(self):
        """ start cpu usage collecting """
        start()
        return "Collect Task Started, <a href='stopCollect'>Click to Stop</a>"
    index.exposed = True

    def stopCollect(self):
        """ stop cpu usage collecting """
        stop()
        return "Stoped!  <a href='../'>Click to Start</a>"
    stopCollect.exposed = True

    def latest(self):
        """ latest cpu usage """
        row = showtable.getLatestRecord()
        if row:
            obj = {'id': row[0], 'kpi': row[1], 'value': row[2],
                    'target': row[3], 'createtime': row[4]}
            return json.dumps(obj)
        else:
            return ""
    latest.exposed = True

    def config(self):
        """ cpu num """
        cpu = str(collecttask.cpuNum())
        return str(cpu)
    config.exposed = True

    def processes(self):
        process_list = collecttask.processes()
        if process_list is None:
            return '[]'
        return json.dumps(process_list)
    processes.exposed = True

    def memory(self):
        memused_percent = collecttask.memory()
        if memused_percent is None:
            return '0'
        return memused_percent
    memory.exposed = True


    #end of CollectData class


def start():
    if status():
        print "Task is already running..."
        return
    collecttask.go()
    print "Collect started..."


def stop():
    collecttask.stop()
    print "Collect stoped"


def status():
    return collecttask.isRunning()


def main():
    if cherrypy_available is False:
        return

    cf = ConfigParser.ConfigParser()
    cf.read(tutconf)
    ip = cf.get("global", "server.socket_host")
    port = cf.getint("global", "server.socket_port")
    ip = ip[1:len(ip) - 1]
    print "server starting at: ", ip + ":" + str(port)
    available = checkPort(ip, port)
    if available is False:
        return

    cherrypy.quickstart(CollectData(), "", tutconf)

    print "server exited!"


def checkPort(ip, port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        skt.bind((ip, port))
        print str(port) + " is available!"
        return True
    except Exception:
        print str(port) + " has already used!"
        return False

# Main
#=====

if __name__ == "__main__":
    main()

# The end...
