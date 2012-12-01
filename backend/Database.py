'''
Copyright (C) 2012 Riccardo Ferrazzo <f.riccardo87@gmail.com>

This file is part of TwitterCrawler.

    TwitterCrawler is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TwitterCrawler is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with TwitterCrawler.  If not, see <http://www.gnu.org/licenses/>
    
'''
import sqlite3, datetime
from queries import *

class DatabaseManager(object):
    
    db = None
    cursor = None
    
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        #self.db = sqlite3.connect("/home/riccardo/TwitterCrawlerdebug.db")
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        self.createDbStructure()
        
    def createDbStructure(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='tweets'")
        if self.cursor.fetchone() == None:
            self.cursor.execute(table_tweets)
            self.cursor.execute(table_locations)
            self.cursor.execute(table_hashtags)
            self.cursor.execute(table_links)
            self.db.commit()
        return
            
    def deleteAll(self):
        self.cursor.execute("DELETE FROM tweets")
        self.cursor.execute("DELETE FROM locations WHERE tweet NOT IN (SELECT distinct id from tweets)")
        self.cursor.execute("DELETE FROM hashtags WHERE tweet NOT IN (SELECT distinct id from tweets)")
        self.cursor.execute("DELETE FROM links WHERE tweet NOT IN (SELECT distinct id from tweets)")
        self.db.commit()

    def addTweet(self, user_name, text, year, month, day, hour, minute, second):
        if self.getTweet(user_name, text) != -1:
            return -1
        self.cursor.execute("INSERT INTO tweets(user_name, text, year, month, day, hour, minute, second) VALUES(?,?,?,?,?,?,?,?)",
                            (user_name, text, year, month, day, hour, minute, second))
        return self.cursor.lastrowid
    
    def addLocation(self, tweet_id, latitude, longitude):
        self.cursor.execute("INSERT INTO locations(tweet, lat, long) VALUES(?, ?, ?)", 
                            (tweet_id, latitude, longitude))
        
    def getStepInfo(self, last_id):
        try:
            self.cursor.execute('''SELECT tweets.id, tweets.user_name, tweets.year, tweets.month, tweets.day, tweets.hour, tweets.minute, tweets.second, tweets.text
            FROM tweets
            WHERE tweets.id>?''', (last_id,))
        except sqlite3.OperationalError:
                pass #TODO: sqlite3.OperationalError: Could not decode to UTF-8 column 'text' with text 'I hope I get this damn job ##non-utf8char
        return self.cursor.fetchall()
    
    def getIdLocation(self, t_id):
        self.cursor.execute('''SELECT lat, long 
        FROM locations
        WHERE tweet = ?''', (t_id,))
        res = self.cursor.fetchone()
        if res == None:
            return {"lat": False, "lon": False}
        return {"lat": res[0], "lon": res[1]}
    
    def addHashtag(self, tweet_id, tag):
        self.cursor.execute("INSERT INTO hashtags(tweet, tag) VALUES(?, ?)", (tweet_id, tag))
    
    def addLink(self, tweet_id, address):
        self.cursor.execute("INSERT INTO links(tweet, address) VALUES(?, ?)", (tweet_id, address))
        
    def getTweet(self, user_name, text):
        self.cursor.execute('SELECT id FROM tweets WHERE user_name = ? AND text = ?', (user_name, text))
        res = self.cursor.fetchone()
        if res == None:
            return -1
        return res[0]
        
    def getUserTweets(self, userName):
        self.cursor.execute('SELECT id FROM tweets WHERE user_name = ? ORDER BY year, month, day, hour, minute, second DESC', (userName,))
        return self.cursor.fetchall()
    
    def dumpDb(self, output):
        f = open(output, 'w')
        for line in self.db.iterdump():
            f.write('%s\n' % line)
        f.close()
        
    def commit(self):
        self.db.commit()
    
if __name__ == "__main__":
    '''used for debug'''
    db = DatabaseManager()
    print db.getUserId("SamDiephuis")