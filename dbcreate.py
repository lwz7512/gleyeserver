# -*- coding: utf-8 *-*
"""
    create the database and table for sqlite3, or mysql(future)
    currently use sqlite3, for mysql database setup,
    use parameter after this file;

    Database name: gleye.db

    Table name: genpfm
    Table structure:
        id,INTEGER PRIMARY KEY
        kpi,TEXT
        value,TEXT
        target,TEXT
        create_time,REAL (float)

    2012/09/26

    Table name: genproc
    Table structure:
        id,INTEGER PRIMARY KEY
        pid,TEXT
        user,TEXT
        nice,TEXT
        virt,TEXT
        res,TEXT
        cpupercent,TEXT
        mempercent,TEXT
        timeaccum,TEXT
        pname,TEXT
        create_time,REAL (float)

    2012/11/04

"""
import sqlite3


dbname = "../sqlite/gleye.db"
pfmtable = "genpfm"
proctable = "genproc"


def createPerformanceTable():
    conn = sqlite3.connect(dbname)
    conn.isolation_level = None
    cur = conn.cursor()
    cur.execute("VACUUM " + pfmtable)
    cur.execute("DROP TABLE IF EXISTS " + pfmtable)
    cur.execute("CREATE TABLE " + pfmtable +
                "(id INTEGER PRIMARY KEY, " +
                "kpi TEXT, value TEXT, target TEXT, create_time REAL)")
    print "table: ", pfmtable, "constructed!"
    cur.close()


def createProcessTable():
    conn = sqlite3.connect(dbname)
    conn.isolation_level = None
    cur = conn.cursor()
    cur.execute("VACUUM " + proctable)
    cur.execute("DROP TABLE IF EXISTS " + proctable)
    cur.execute("CREATE TABLE " + proctable +
                "(id INTEGER PRIMARY KEY, " +
                "pid TEXT, user TEXT, nice TEXT, " +
                "vert TEXT, res TEXT, cpupercent TEXT, mempercent TEXT, " +
                "timeaccum TEXT, pname TEXT, create_time REAL)")
    print "table: ", proctable, "constructed!"
    cur.close()


def testInsertData():
    conn = sqlite3.connect(dbname)
    conn.isolation_level = None  # use this, or use conn.commi()
    cur = conn.cursor()
    cur.execute("INSERT INTO " + pfmtable +
            "(kpi,value,target,create_time) " +
            "VALUES('cpu_usage','0.1','samplehost','123')")
    cur.close()
    print "inserted one sample record:"


def testDatabseAvail():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + pfmtable)
    for row in cur.fetchall():
        print row
    cur.close()


def main():
    # TODO, auto create sqlite dir...
    createPerformanceTable()
    createProcessTable()
    #todo, add other table...


# Main
#=====

if __name__ == "__main__":
    main()

# The end...
