# -*- coding: utf-8 *-*
"""
    insert, modify, delete, query, VACUUM

    2012/09/26
"""
import sqlite3


class SqliteQuery:

    def __init__(self, dbName):
        self.dbName = dbName
        self.con = sqlite3.connect(dbName)
        self.cur = self.con.cursor()

    def __del__(self):
        try:
            self.cur.close()
        except Exception as inst:
            print "clean cursor error:"
            print inst

    def create(self, tableName, fields):
        self.tableName = tableName
        self.cur.execute("DROP TABLE IF EXISTS " + tableName)
        self.cur.execute("CREATE TABLE " + tableName + "(" + fields + ")")
        self.cur.close()

    def table(self, tableName):
        self.tableName = tableName
        return self

    def insert(self, fieldsTpl, valuesTpl):
        if self.validateTable() is False:
            return
        try:
            self.cur = self.con.cursor()
            self.cur.execute("INSERT INTO " + self.tableName +
                repr(fieldsTpl) + " VALUES " + repr(valuesTpl))
        except Exception as inst:
            print "Warning,insert record error:"
            print inst
        finally:
            self.con.commit()
            self.cur.close()

    def delete(self, where):
        if self.validateTable() is False:
            return
        try:
            self.cur = self.con.cursor()
            if where:
                self.cur.execute("DELETE FROM " + self.tableName +
                            "WHERE " + where)
            else:
                self.cur.execute("DELETE FROM " + self.tableName)
        except Exception as inst:
            print "Warning,delete record error!"
            print inst
        finally:
            self.con.commit()
            self.cur.close()

    def update(self, fieldsTpl, valuesTpl):
        pass  # TODO,...

    def query(self, fieldsTpl, where):
        if self.validateTable() is False:
            return
        try:
            self.cur = self.con.cursor()
            if where:
                self.cur.execute("SELECT " + fieldsTpl +
                            " FROM " + self.tableName + "WHERE " + where)
            else:
                self.cur.execute("SELECT " + fieldsTpl +
                            " FROM " + self.tableName + " LIMIT 10")
            rows = self.cur.fetchall()
        except Exception as inst:
            print "Warning, query record error:"
            print inst
        finally:
            self.cur.close()

        return rows  # list

    def validateTable(self):
        try:
            self.tableName
        except Exception:
            print "tableName is not assigned, stop query..."
            return False
        return True

    def clean(self):
        self.__del__()

# end of SqliteQuery definition


def test():
    # sample database create...
    query = SqliteQuery(":memory:")
    query.create("sampletable", "name TEXT, age INTEGER")
    print "create sample table success..."

    # test data insert in memory...
    #query.table("sampletable")
    query.insert(('name', 'age'), ('lwz7512', 37))
    print "insert one row success..."

    # test data query in memory...
    rows = query.query("name, age", None)
    for row in rows:
        print row

    # test data delete in memory...
    query.delete(None)
    print "delete all rows success!"

    # test clean...
    query.clean()
    print "clean cursor success!"
# Main
#=====

if __name__ == "__main__":
    test()

# The end...
