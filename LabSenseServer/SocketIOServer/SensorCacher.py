import sqlite3
import time

class SensorCacher:
    def __init__(self):
        self.conn = sqlite3.connect('cache.db')
        self.cursor = self.conn.cursor()
        self.max_entries = 2

    def createTable(self, channel):
        if not self.checkTableExists(channel):
            self.cursor.execute(""" CREATE TABLE %s (name text, data text, time
                    text, timestamp real)""" % channel)

    def checkTableExists(self, table):
        self.cursor.execute(""" SELECT name FROM sqlite_master WHERE type='table' AND name="%s" """ % table)
        if self.cursor.fetchone() == None:
            return False
        else:
            return True


    def insertRow(self, channel, name, data, timestamp):
        insertion = """ INSERT INTO %s VALUES ("%s","%s", "%s", %f)""" % (channel, name, data, str(timestamp), timestamp)
        self.cursor.execute(insertion)

        self.conn.commit()

    def getChannelData(self, channel, name):
        try:
            self.cursor.execute("SELECT * FROM '%s'" % (channel))
            results = self.cursor.fetchall()
        except sqlite3.Error, e:
            return []

        if len(results) > self.max_entries:
            print "DELETING"
            self.cursor.execute("DELETE FROM %s WHERE rowid = (SELECT rowid FROM %s\
                    order by rowid limit 5)" % (channel, channel))

        return results




if __name__ == "__main__":
    s = SensorCacher()
    s.createTable("Raritan")
    s.insertRow("Raritan", "Raritan_Current_1", "0.4", time.time())
    s.insertRow("Raritan", "Raritan_Current_1", "0.5", time.time())
    s.insertRow("Raritan", "Raritan_Current_1", "0.6", time.time())

    results = s.getChannelData("Raritan", "Raritan_Current_1")
    print results

    time.sleep(2);

    results = s.getChannelData("Raritan", "Raritan_Current_1")
    print results


