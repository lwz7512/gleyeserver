# -*- coding: utf-8 *-*
"""
    print the data by assign the db tablename, in console

    2012/09/26
"""
import sqlite3
from dboperate import SqliteQuery


dbname = "gleye.db"
tbname = "genpfm"
colswidth = [13, 11, 13, 14, 19]


def showTableSchema():
    con = sqlite3.connect(dbname)
    cur = con.execute("PRAGMA table_info(" + tbname + ")")
    rows = cur.fetchall()
    for col in rows:
        print col[1] + "(" + col[2] + ")  ",  # connect with next line...
    print ""
    print "................................................" * 2


def printTableData():
    query = SqliteQuery(dbname)
    query = query.table(tbname)
    rows = query.query("*", None)
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