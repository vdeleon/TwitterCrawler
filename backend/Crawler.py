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
from RestCrawler import *
from StreamingCrawler import *
from PySide.QtCore import *
from Database import DatabaseManager
import tweepy

CONSUMER_KEY = "JmaTtQcCQUjz9YzTfB3FbQ"
CONSUMER_SECRET = "9dqYHe7P1R22UqbhzukpX5WUGZwYOVCM9OkgUsQMpUI"

REST_CRAWLER = 1
STREAMING_CRAWLER = 2

class Crawler(QObject, AbstractCrawler):
    def __init__(self):
        QObject.__init__(self)
        AbstractCrawler.__init__(self)
        self.settings = QSettings("RFCode", "TwitterCrawler")
        self.db = DatabaseManager()
        self.rest = None
        self.streaming = None
        self.auth = None
        self.threadPool = []
        
    def authInit(self):
        self.rest = RestCrawler(self.auth)
        self.streaming = StreamingCrawler(self.auth, headers={"User-Agent": "TwitterCrawler/1.0"})
        self.rest.restDataReady.connect(self.updateSearchStep)
        self.streaming.listener.streamingDataReady.connect(self.updateSearchStep)
        self.streaming.listener.streamingError.connect(self.errorHandler)
    
    def getAuthUrl(self):
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        return self.auth.get_authorization_url()
    
    def setAuthAccess(self, verifier):
        self.auth.get_access_token(verifier)
        self.settings.setValue("auth_key", self.auth.access_token.key)
        self.settings.setValue("auth_secret", self.auth.access_token.secret)
            
    def login(self):
        key = self.settings.value("auth_key")
        secret = self.settings.value("auth_secret")
        if key == None or secret == None:
            return False
        if self.auth == None:
            self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(key, secret)
        self.authInit()
        return True
    
    @Slot(int)
    def errorHandler(self, code):
        print "error", code
        if code >= 600:
            return;
        self.stop()
#        if code == 420: #rate limit error
#            pass #TODO
#        elif code == 600: #streaming parsing error
#            pass 
#        elif code == 601: #database insertion error
#            pass
    
    @Slot("QVariant")
    def updateSearchStep(self, step):
        for tweet in step:
            dbId = self.db.addTweet(tweet["userName"], 
                                    tweet["tweet"], 
                                    tweet["year"], 
                                    tweet["month"], 
                                    tweet["day"], 
                                    tweet["hour"], 
                                    tweet["minute"], 
                                    tweet["second"])
            for h in tweet["hashtags"]:
                self.db.addHashtag(dbId, h)
            for l in tweet["links"]:
                self.db.addLink(dbId, l)
            if tweet["location"] != False:
                self.db.addLocation(dbId, tweet["location"]["lat"], tweet["location"]["lon"])
            tweet["dbId"] = dbId
        self.db.commit()
    
    def getTweetsInsideArea(self, lat1, lon1, lat2, lon2, crawler=REST_CRAWLER|STREAMING_CRAWLER, **parameters):
        '''Get tweets inside the given bounding box'''
        if (crawler&REST_CRAWLER) == REST_CRAWLER:
            self.threadPool.append(MyThread(self.rest.getTweetsInsideArea, lat1, lon1, lat2, lon2, **parameters))
        if (crawler&STREAMING_CRAWLER) == STREAMING_CRAWLER:
            self.streaming.getTweetsInsideArea(lat1, lon1, lat2, lon2, **parameters)
        
    def getTweetsByContent(self, content, crawler=REST_CRAWLER|STREAMING_CRAWLER, **parameters):
        if (crawler&REST_CRAWLER) == REST_CRAWLER:
            self.threadPool.append(MyThread(self.rest.getTweetsByContent, content, **parameters))
        if (crawler&STREAMING_CRAWLER) == STREAMING_CRAWLER:
            self.streaming.getTweetsByContent(content)
            
    def getTweetsByUser(self, username, crawler=REST_CRAWLER|STREAMING_CRAWLER, **parameters):
        if(crawler&REST_CRAWLER) == REST_CRAWLER:
            self.threadPool.append(MyThread(self.rest.getTweetsByUser, username, **parameters))
        if (crawler&STREAMING_CRAWLER) == STREAMING_CRAWLER:
            self.streaming.getTweetsByUser(username, **parameters)

    def stop(self):
        self.streaming.stop()
        self.db.commit()