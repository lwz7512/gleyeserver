# -*- coding: utf-8 *-*
"""
This is a starter app for a series of monitoring products, aiming to realtime
check the server/database/business running status, first use ubuntu to test!

    2012/09/19 by lwz7512

"""
# Libraries
#==========
import json
import os.path

import cherrypy

import showtable
import collecttask

localDir = os.path.dirname(__file__)
tutconf = os.path.join(localDir, 'server.conf')


class CollectData:

    def index(self):
        start()
        return "Collect Task Started, <a href='stopCollect'>Click to stop</a>"
    index.exposed = True

    def stopCollect(self):
        stop()
        return "Stoped!  <a href='../'>click to start</a>"
    stopCollect.exposed = True

    def latest(self):
        row = showtable.getLatestRecord()
        if row:
            obj = {'id': row[0], 'kpi': row[1], 'value': row[2],
                    'target': row[3], 'createtime': row[4]}
            return json.dumps(obj)
        else:
            return ""
    latest.exposed = True

    def config(self):
        cpu = str(collecttask.cpuNum())
        return str(cpu)
    config.exposed = True

    #end of CollectData class


def hostCfg():
    return collecttask.cpuNum()


def start():
    if collecttask.isRunning():
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
    cherrypy.quickstart(CollectData(), config=tutconf)

# Main
#=====

if __name__ == "__main__":
    main()

# The end...
