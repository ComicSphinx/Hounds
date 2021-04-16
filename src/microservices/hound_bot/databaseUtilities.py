# @Author: Daniil Maslov (Comicsphinx)

import sqlite3
import os
import sys

database_file_path = "database.db"
tableName = " users "

def verifyDatabaseExist():
    if (os.path.exists(database_file_path)):
        return 1
    else:
        return 0

def createDB():
    connection, cursor = connectDB()
    request = "CREATE TABLE"+tableName+"(chat_uid int, portfolio_url VARCHAR(50), goal_profit int);"
    executeRequest(request)
    output = saveAndCloseDB(connection)
    print("db created")

def connectDB():
    connection = sqlite3.connect(database_file_path)
    cursor = connection.cursor()
    return connection, cursor

def saveAndCloseDB(connection):
    connection.commit()
    connection.close()

def executeRequest(request):
    connection, cursor = connectDB()
    cursor.execute(request)
    output = cursor.fetchall()
    saveAndCloseDB(connection)
    return output

def addData(chat_uid, column, data):
    print(chat_uid, "attempts to add data")
    request = "UPDATE" + tableName + "SET " + str(column) + " = '" + str(data) + "' WHERE chat_uid = " + str(chat) 
    if (verifyDBContainsChat(chat_uid) == 1):
        print(chat_uid, "Using request :", request)
        executeRequest(request)
        print(chat_uid, "Data successfully added")
    elif (verifyDBContainsChat(chat_uid) == 0):
        print(chat_uid, "user not found, user will be added")
        addUser(chat_uid)
        print(chat_uid, "user added to db")
        executeRequest(request)
        print(chat_uid, "data successfully added")
    else:
        print("Unrecognized error")

def addUser(chat_uid):
    if (verifyDBContainsChat(chat_uid) == 0):
        request = "INSERT INTO" + tableName + "(" + "chat_uid" + ")" + "VALUES (" + str(chat_uid) + ");"
        executeRequest(request)
        print(chat_uid, "user successfully added")

def verifyDBContainsChat(chat_uid):
    output = get_user(chat_uid)
    if (output == []):
        print("DB does not contains chat :", chat_uid)
        return 0
    else:
        print("DB contains chat :", chat_uid)
        return 1

def get_user(chat_uid):
    request = "SELECT * FROM"+tableName+"WHERE chat_uid ="+str(chat_uid)
    connection, cursor = connectDB()
    output = executeRequest(request)
    return output

def test():
    print("test")
    return "test"