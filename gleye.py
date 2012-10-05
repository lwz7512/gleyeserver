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


tutconf = os.path.join(os.path.dirname(__file__), 'server.conf')


class CollectData:

    def index(self):
        start()
        return "<a href='stopCollect'>Click to stop</a>"
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


def start():
    collecttask.go()


def stop():
    collecttask.stop()


def status():
    return collecttask.isRunning()


def main():
    cherrypy.quickstart(CollectData(), config=tutconf)


# Main
#=====

if __name__ == "__main__":
    main()

# The end...
