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
from datetime import timedelta

import dboperate

#global var definition
psutil_available = None
timer = None

dbname = "../sqlite/gleye.db"
tbname = "genpfm"

try:
    import psutil
except ImportError:
    print 'PsUtil module not found. Gleye cannot start.'
    print ''
    print 'On Ubuntu 12.04 or higher:'
    print '$ sudo apt-get install python-psutil'
    print ''
    print 'or install PsUtil using pip (as root):'
    print '# pip install psutil'
    print ''
    psutil_available = False
else:
    print 'pstuil is ready to run...'
    psutil_available = True

    #cpu_num = psutil.NUM_CPUS
    #print 'cpu num: ', cpu_num
#......................... end of test ...................

#--------------- start of Timer class -------------------------


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
            self.__do()
            time.sleep(self.sleep)

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
        #print "timer stoped!"
#............... end of timer class ................................


#--------------- start of private collect functhion -------------


def __collect():
    if psutil_available is False:
        print "psutil is inavailable, could not collect data..."
        return
    __poll_avg_cpu()
    #__poll_per_cpu()


def __poll_avg_cpu():
    cpu_usage = psutil.cpu_percent()
    #save to database...
    query = dboperate.SqliteQuery(dbname)
    query = query.table(tbname)
    #create_milisec = str(math.trunc(time.time() * 1000))
    query.insert(('kpi', 'value', 'target', 'create_time'),
                 ('cpu_usage', str(cpu_usage), 'local', time.time()))
    query.clean()


def __poll_per_cpu():
    # non-blocking (percentage since last call)
    per_cpu_usage = psutil.cpu_percent(0, True)
    for i in range(len(per_cpu_usage)):
        per_cpu_usage[i] = str(per_cpu_usage[i])
    cpu_comma = ','.join(per_cpu_usage)
    #save to database...
    query = dboperate.SqliteQuery(dbname)
    query = query.table(tbname)
    #create_milisec = str(math.trunc(time.time() * 1000))
    query.insert(('kpi', 'value', 'target', 'create_time'),
                 ('cpu_usage', cpu_comma, 'local', time.time()))
    query.clean()


def __poll_total_cpu():
    # non-blocking (percentage since last call)
    cpu_usage = psutil.cpu_percent(interval=0)

    return cpu_usage


def __poll_process_info():
    procs = []
    for p in psutil.process_iter():
        try:
            p.dict = p.as_dict(['username', 'get_nice', 'get_memory_info',
                                'get_memory_percent', 'get_cpu_percent',
                                'get_cpu_times', 'name', 'status'])
        except psutil.NoSuchProcess:
            pass
        else:
            procs.append(p)
    # return processes sorted by CPU percent usage
    stdpss = sorted(procs, key=lambda p: p.dict['cpu_percent'], reverse=True)
    # result process list include calculated value
    result_procs = []
    for p in stdpss:
        # TIME+ column shows process CPU cumulative time and it
        # is expressed as: "mm:ss.ms"
        if p.dict['cpu_times'] is not None:
            ctime = timedelta(seconds=sum(p.dict['cpu_times']))
            ctime = "%s:%s.%s" % (ctime.seconds // 60 % 60,
                                  str((ctime.seconds % 60)).zfill(2),
                                  str(ctime.microseconds)[:2])
        else:
            ctime = ''
        if p.dict['memory_percent'] is not None:
            p.dict['memory_percent'] = round(p.dict['memory_percent'], 1)
        else:
            p.dict['memory_percent'] = ''
        if p.dict['cpu_percent'] is None:
            p.dict['cpu_percent'] = ''
        # create desired process info dict
        result_p = {
            "pid": p.pid,
            "user": p.dict['username'][:8],
            "nice": p.dict['nice'],
            "virt": bytes2human(getattr(p.dict['memory_info'], 'vms', 0)),
            "res": bytes2human(getattr(p.dict['memory_info'], 'rss', 0)),
            "cpupercent": p.dict['cpu_percent'],
            "mempercent": p.dict['memory_percent'],
            "timeaccum": ctime,
            "pname": p.dict['name'] or ''}
        result_procs.append(result_p)

    # only use first 10 process
    return result_procs[:10]


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n


def __poll_memeory_usage_percent():
    mem = psutil.virtual_memory()
    return str(mem.percent)


#..............this is end of collect method..............................


#--------------- start of public functhion -------------------------


def memory():
    if psutil_available is False:
        return None
    return __poll_memeory_usage_percent()


def processes():
    if psutil_available is False:
        return None
    return __poll_process_info()


def cpuNum():
    if psutil_available is False:
        print "psutil is inavailable, could not collect data..."
        return 0
    return psutil.NUM_CPUS


def isRunning():
    global timer
    if timer is not None:
        return timer.isPlay
    return False


def stop():
    global timer
    if timer:
        timer.stop()


def go():
    global timer
    timer = Timer(__collect, (), 3, False)
    timer.start()
    #print 'collect task start to run...'
    #timer.join()  # stop main process finished..

#.................... end of module .................

if __name__ == "__main__":
    go()