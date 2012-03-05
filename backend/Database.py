'''
Created on 28/feb/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import tweepy, os
from time import time
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
        self.createDbStructure()
        
    def createDbStructure(self):
        query = QSqlQuery()
        query.exec_("SELECT name FROM sqlite_master WHERE type='table' and name='users'")
        if not query.first():
            query = QSqlQuery()
            query.exec_(table_searches)
            query.exec_(table_users)
            query.exec_(table_followers)
            query.exec_(table_locations)
            query.exec_(table_hashtags)
            query.exec_(table_links)
            
    def deleteOrphans(self):
        query = QSqlQuery()
        query.exec_("DELETE FROM users WHERE search NOT IN (SELECT distinct id from searches)")
        query.exec_("DELETE FROM followers WHERE user NOT IN (SELECT distinct id from users) OR follower NOT IN (SELECT distinct id from users)")
        query.exec_("DELETE FROM locations WHERE user NOT IN (SELECT distinct id from users)")
        query.exec_("DELETE FROM hashtags WHERE user NOT IN (SELECT distinct id from users)")
        query.exec_("DELETE FROM links WHERE user NOT IN (SELECT distinct id from users)")
        
    def createSearch(self, descr):
        query = QSqlQuery()
        query.prepare("INSERT INTO searches(date, descr) VALUES(:date, :descr)")
        query.bindValue(":date", int(time()))
        query.bindValue(":descr", descr)
        query.exec_()
                
    def deleteSearch(self, search_id):
        query = QSqlQuery()
        query.prepare(delete_search)
        query.bindValue(":id", search_id)
        query.exec_()
        self.deleteOrphans()
        
    def deleteLastSearch(self):
        query = QSqlQuery()
        query.exec_("SELECT max(id) FROM searches")
        query.first()
        self.deleteSearch(query.value(0))
    
    def addSearchStep(self, search_id):
        query = QSqlQuery()
        query.prepare(add_search_step)
        query.bindValue(":ida", search_id)
        query.bindValue(":idb", search_id)
        query.exec_()
    
    def addUser(self, t_id, t_screen_name, search_id, step):
        query = QSqlQuery()
        query.prepare("INSERT INTO users(t_id, t_screen_name, search, step) VALUES(:t_id, :t_screen_name, :search_id, :step)")
        query.bindValue(":t_id", t_id)
        query.bindValue(":t_screen_name", t_screen_name)
        query.bindValue(":search_id", search_id)
        query.bindValue(":step", step)
        query.exec_()
        
    def getUserId(self, **kwargs):
        '''kwarg can be only t_id or t_screen_name'''
        var = kwargs.keys()[0]
        if var not in ["t_id", "t_screen_name"]:
            raise Exception("Wrong variable it can be only t_id or t_screen_name")
        query = QSqlQuery()
        query.prepare("SELECT id FROM users WHERE :variable=:value")
        query.bindValue(":variable", var)
        query.bindValue(":value", kwargs[var])
        query.exec_()
        query.first()
        return query.value(0)
        
    def addFollower(self, t_id, t_screen_name, search_id, step, user_id):
        self.addUser(t_id, t_screen_name, search_id, step)
        follower_id = self.getUserId(t_id=t_id)
        query = QSqlQuery()
        query.prepare("INSERT INTO followers(user, follower) VALUES(:user, :follower)")
        query.bindValue(":user", user_id)
        query.bindValue(":follower", follower_id)
        query.exec_()
    
    def addLocation(self, user_id, date, latitude, longitude):
        query = QSqlQuery()
        query.prepare("INSERT INTO locations(user, date, lat, long) VALUES(:user, :date, :lat, :long)")
        query.bindValue(":user", user_id)
        query.bindValue(":date", date)
        query.bindValue(":lat", latitude)
        query.bindValue(":long", longitude)
        query.exec_()
    
    def addHashtag(self, user_id, tag):
        query = QSqlQuery()
        query.prepare("INSERT INTO hashtags(user, tag) VALUES(:user, :tag)")
        query.bindValue(":user", user_id)
        query.bindValue(":tag", tag)
        query.exec_()
    
    def addLink(self, user_id, address):
        query = QSqlQuery()
        query.prepare("INSERT INTO links(user, address) VALUES(:user, :address)")
        query.bindValue(":user", user_id)
        query.bindValue(":address", address)
        query.exec_()       
    
if __name__ == "__main__":
    '''used for debug'''
    db = DatabaseManager()
    db.deleteLastSearch()