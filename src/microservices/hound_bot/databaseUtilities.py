# @Author: Daniil Maslov (Comicsphinx)

import sqlite3
import os
import sys

database_file_path = "database.db"
tableName = " users_data "

def verifyDatabaseExist(self):
    if (os.path.exists(self.database_file_path)):
        return 1
    else:
        return 0

def createDB(self):
    connection, cursor = self.connectDB(self)
    cursor.execute("CREATE TABLE"+self.tableName+"(tg_uid int, parse_link VARCHAR(50), goal_profit int, auto_update_time int);")
    self.saveAndCloseDB(self, connection)

def connectDB(self):
    connection = sqlite3.connect(self.database_file_path)
    cursor = connection.cursor()
    return connection, cursor

def saveAndCloseDB(self, connection):
    connection.commit()
    connection.close()

def executeCommand(self, insert):
    connection, cursor = self.connectDB(self)
    cursor.execute(insert)
    output = cursor.fetchall()
    self.saveAndCloseDB(self,connection)
    return output