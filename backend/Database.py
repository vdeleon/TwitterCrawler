'''
Created on 28/feb/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import tweepy, os
from time import time
import sqlite3 as sqlite
from queries import *

class DatabaseManager(object):
    def __init__(self):
        #self.db = sqlite.connect(":memory:")
        self.db = sqlite.connect("debug.db")
        self.db.row_factory = sqlite.Row
        self.cursor = self.db.cursor()
        self.createDbStructure()
        
    def createDbStructure(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='users'")
        if self.cursor.fetchone() == None:
            self.cursor.execute(table_searches)
            self.cursor.execute(table_users)
            self.cursor.execute(table_followers)
            self.cursor.execute(table_locations)
            self.cursor.execute(table_hashtags)
            self.cursor.execute(table_links)
            self.db.commit()
            
    def deleteOrphans(self):
        self.cursor.execute("DELETE FROM users WHERE search NOT IN (SELECT distinct id from searches)")
        self.cursor.execute("DELETE FROM followers WHERE user NOT IN (SELECT distinct id from users) OR follower NOT IN (SELECT distinct id from users)")
        self.cursor.execute("DELETE FROM locations WHERE user NOT IN (SELECT distinct id from users)")
        self.cursor.execute("DELETE FROM hashtags WHERE user NOT IN (SELECT distinct id from users)")
        self.cursor.execute("DELETE FROM links WHERE user NOT IN (SELECT distinct id from users)")
        self.db.commit()
        
    def __getLastSearchId(self):
        self.cursor.execute('SELECT max("id") FROM "searches"')
        return self.cursor.fetchone()[0]
    
    def tmp(self):
        return self.__getLastSearchId()
        
    def createSearch(self, descr):
        self.cursor.execute("INSERT INTO searches(date, descr) VALUES(?, ?)", (int(time()), descr))
        self.db.commit()
        return self.__getLastSearchId()
                
    def deleteSearch(self, search_id):
        self.cursor.execute("DELETE FROM searches WHERE id=?", (search_id,))
        self.db.commit()
        self.deleteOrphans()
        
    def deleteLastSearch(self):
        self.deleteSearch(self.__getLastSearchId())
    
    def addSearchStep(self, search_id):
        self.cursor.execute(add_search_step, (search_id, search_id))
        self.db.commit()
    
    def addUser(self, t_id, t_screen_name, search_id, step):
        self.cursor.execute("INSERT INTO users(t_id, t_screen_name, search, step) VALUES(?, ?, ?, ?)",
                            (t_id, t_screen_name, search_id, step))
        self.db.commit()
        
    def getUserId(self, **kwargs):
        '''kwarg can be only t_id or t_screen_name'''
        var = kwargs.keys()[0]
        if var not in ["t_id", "t_screen_name"]:
            raise Exception("Wrong variable it can be only t_id or t_screen_name")
        self.cursor.execute('SELECT id FROM users WHERE ?=?', (var, kwargs[var]))
        return self.cursor.fetchone()[0]
        
    def addFollower(self, t_id, t_screen_name, search_id, step, user_id):
        self.addUser(t_id, t_screen_name, search_id, step)
        follower_id = self.getUserId(t_id=t_id)
        self.cursor.execute("INSERT INTO followers(user, follower) VALUES(?, ?)", (user_id, follower_id))
        self.db.commit()
    
    def addLocation(self, user_id, date, latitude, longitude):
        self.cursor.execute("INSERT INTO locations(user, date, lat, long) VALUES(?, ?, ?, ?)", 
                            (user_id, date, latitude, longitude))
        self.db.commit()
    
    def addHashtag(self, user_id, tag):
        self.cursor.execute("INSERT INTO hashtags(user, tag) VALUES(?, ?)", (user_id, tag))
        self.db.commit()
    
    def addLink(self, user_id, address):
        self.cursor.execute("INSERT INTO links(user, address) VALUES(?, ?)", (user_id, address))
        self.db.commit()
    
if __name__ == "__main__":
    '''used for debug'''
    db = DatabaseManager()
    print db.tmp()