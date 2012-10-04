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
        create_time,INTEGER (long miliseconds)

    2012/09/26

"""
import sqlite3


dbname = "../sqlite/gleye.db"
tbname = "genpfm"


def createPerformanceTable():
    conn = sqlite3.connect(dbname)
    conn.isolation_level = None
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS " + tbname)
    cur.execute("CREATE TABLE " + tbname +
                "(id INTEGER PRIMARY KEY, " +
                "kpi TEXT, value TEXT, target TEXT, create_time INTEGER)")
    print "table: ", tbname, "constructed!"
    #conn.commit()
    cur.close()


def testInsertData():
    conn = sqlite3.connect(dbname)
    conn.isolation_level = None  # use this, or use conn.commi()
    cur = conn.cursor()
    cur.execute("INSERT INTO " + tbname +
            "(kpi,value,target,create_time) " +
            "VALUES('cpu_usage','0.1','samplehost','12345')")
    #conn.commit()  # a must do, or cannot see results
    cur.close()
    print "inserted one sample record:"


def testDatabseAvail():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + tbname)
    print cur.fetchone()
    cur.close()


def main():
    createPerformanceTable()
    testInsertData()
    testDatabseAvail()
    #todo, add other table...


# Main
#=====

if __name__ == "__main__":
    main()

# The end...
