# -*- coding: utf-8 *-*
"""
    Run time-related task, including the main collect implementaion;
    This is an abstract collect class, for specific kpi;
    Expose the method:
        run(),start to collect;
        poll(),the main collect logic;
        stop(),stop the collect task;

"""
import threading
import time

psutil_available = None
cpu_num = None
timer = None
running = False

try:
    import psutil
except ImportError:
    print 'PsUtil module not found. Glances cannot start.'
    print ''
    print 'On Ubuntu 12.04 or higher:'
    print '$ sudo apt-get install python-psutil'
    print ''
    print 'To install PsUtil using pip (as root):'
    print '# pip install psutil'
    print ''
    psutil_available = False
else:
    print 'pstuil is ready...'
    psutil_available = True
    cpu_num = psutil.NUM_CPUS
    print 'cpu num: ', cpu_num


def isRunning():
    if timer is not None:
        return timer.isPlay
    return False


def collect():
    if psutil_available is False:
        return
    poll_per_cpu()


def poll_total_cpu():
    # non-blocking (percentage since last call)
    cpu_usage = psutil.cpu_percent(interval=0)

    return cpu_usage


def poll_per_cpu():
    # non-blocking (percentage since last call)
    per_cpu_usage = psutil.cpu_percent(0, True)
    cpu_usage_all = []
    for i in per_cpu_usage:
        cpu_usage_all.append(str(i) + ',')
    cpu_striped = ''.join(cpu_usage_all)
    cpu_striped = cpu_striped[:len(cpu_striped) - 1]
    print 'cpu usage: ', cpu_striped
    #TODO, save to database...


def poll_process_info():
    pass    # TODO, ...

#..............this is end of collect method..............................


class Timer(threading.Thread):

    def __init__(self, fn, args=(), sleep=0, lastDo=True):
        threading.Thread.__init__(self)
        self.fn = fn
        self.args = args
        self.sleep = sleep
        self.lastDo = lastDo
        self.setDaemon(True)

        self.isPlay = True
        self.fnPlay = False

    def __do(self):
        self.fnPlay = True
        apply(self.fn, self.args)
        self.fnPlay = False

    def run(self):
        while self.isPlay:
            time.sleep(self.sleep)
            self.__do()

    def stop(self):
        #stop the loop
        self.isPlay = False
        while True:
            if not self.fnPlay:
                break
            time.sleep(0.01)
        #if lastDo,do it again
        if self.lastDo:
            self.__do()


def stop():
    if timer is not None:
        timer.stop()


def go():
    timer = Timer(collect, (), 3, False)
    timer.start()
    print 'collect task start to run...'
    timer.join()  # stop main finished..


if __name__ == "__main__":
    go()