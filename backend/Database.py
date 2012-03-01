'''
Created on 28/feb/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import tweepy, os
from PySide.QtSql import *
from queries import *

class QDbException(Exception):
    def __init__(self, qSqlError):
        self.msg = ""
        if qSqlError.type() == QSqlError.ConnectionError:
            self.msg = "Connection error"
        elif qSqlError.type() == QSqlError.StatementError:
            self.msg = "SQL statement syntax error"
        elif qSqlError.type() == QSqlError.TransactionError:
            self.msg = "Transaction failed error"
        elif qSqlError.type() == QSqlError.UnknownError:
            self.msg = "Unknown Error"
        
    def __str__(self):
        return self.msg

class DatabaseManager(object):
    def __init__(self, dbFolder="."):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        dbName = os.path.join(dbFolder, "twittercrawler.db")
        self.db.setDatabaseName(dbName)
        if not self.db.open():
            raise QDbException(self.db.lastError())
        self.createDatabaseStructure()
        
    def createDbStructure(self):
        query = QSqlQuery()
        query.exec_("SELECT name FROM sqlite_master WHERE type='table' and name='users'")
        if not query.next():
            query = QSqlQuery()
            query.exec_(table_creation)
    
    def deleteSearch(self, id):
        query = QSqlQuery()
        query.prepare(delete_search)
        query.bindValue("id", id)
        query.exec_()
    
    def deleteLastSearch(self):
        pass
    
    
        
        
        