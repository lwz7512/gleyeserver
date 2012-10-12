# -*- coding: utf-8 *-*
"""
    print the data by assign the db tablename, in console

    2012/09/26
"""
import datetime
import time
import sqlite3
from dboperate import SqliteQuery


dbname = "../sqlite/gleye.db"
tbname = "genpfm"
colswidth = [13, 11, 13, 14, 19]


# used by collecttask...
def getLatestRecord():
    query = SqliteQuery(dbname)
    query = query.table(tbname)
    endtime = time.time()
    # every 3 second to collect cpu, and consume ~0.18 to run task,
    # so have a little lag, to query the right data, consider the factor
    # 2012/10/11
    starttime = endtime - 3.2
#where = "create_time >" + str(starttime) + " AND create_time <" + str(endtime)
    where = "create_time >:starttime AND create_time <:endtime"
    params = {"starttime": starttime, "endtime": endtime}
    rows = query.query("*", where, params)
    #print "latest record: "
    if rows:
        return rows[0]
    else:
        return None


def timeToSimpleFormatDate(sec):
    dt = datetime.datetime.fromtimestamp(sec)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


# ------------------test method to show saved data-----------------
def showTableSchema():
    con = sqlite3.connect(dbname)
    cur = con.execute("PRAGMA table_info(" + tbname + ")")
    rows = cur.fetchall()
    for col in rows:
        print col[1] + "(" + col[2] + ")  ",  # connect with next line...
    print ""
    print "-------------------------------------------" * 2


def printTableData():
    query = SqliteQuery(dbname)
    query = query.table(tbname)
    rows = query.query("*", None, None, "create_time", 10)
    if rows is None:
        print "results is none, stop to display..."
        return

    for row in rows:
        for i in range(len(row)):
            print str(row[i]) + " " * (colswidth[i] - len(str(row[i]))),
        print ""  # this is end of each row...


def main():
    showTableSchema()
    printTableData()


if __name__ == "__main__":
    main()