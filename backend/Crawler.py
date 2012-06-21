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
from Database import *
from PySide.QtCore import *
import tweepy

CONSUMER_KEY = "JmaTtQcCQUjz9YzTfB3FbQ"
CONSUMER_SECRET = "9dqYHe7P1R22UqbhzukpX5WUGZwYOVCM9OkgUsQMpUI"

class Crawler(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.settings = QSettings("rferrazz", "TwitterCrawler")
        self.db = DatabaseManager()
        self.rest = None
        self.streaming = None
        self.auth = None
        self.search = None
        self.threadPool = []
        
    def authInit(self):
        self.rest = RestCrawler(self.auth)
        self.streaming = StreamingCrawler(self.auth)
        self.rest.restDataReady.connect(self.updateSearchStep)
        self.streaming.listener.streamingDataReady.connect(self.updateSearchStep)
    
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
    
    def createSearch(self):
        self.search = self.db.createSearch("Tmp")
        
    def addSearchStep(self):
        self.db.addSearchStep(self.search)
        
    def getSteps(self):
        if self.search == None:
            return 0
        return self.db.getSteps(self.search)
        
    @Slot("QVariant")
    def updateSearchStep(self, step):
        for u in step["users"]:
            self.db.addUser(u["userId"], u["userName"], self.search, self.step)
            for f in u["followers"]:
                self.db.addFollower(f["userId"], f["userName"], self.search, self.step, self.db.getUserId(t_screen_name=u["userName"]))
        for t in step["tweets"]:
            self.db.addUser(t["userId"], t["userName"], self.search, self.step)
            userId = self.db.getUserId(t["userName"])
            if t["location"] != None:
                self.db.addLocation(userId, t["time"], t["location"][0], t["location"][1])
            for tag in t["hashtags"]:
                self.db.addHashtag(userId, tag)
            for link in t["links"]:
                self.db.addLink(userId, link)
    
    def trackTweetsInsideArea(self, lat1, lon1, lat2, lon2):
        '''Get tweets inside the given bounding box'''
        width = abs(lat2-lat1)
        height = abs(lon2-lon1)
        if lat1 < lat2:
            lat = lat1
        else:
            lat = lat2
        if lon1 < lon2:
            lon = lon1
        else:
            lon = lon2
        if self.rest.isEnabled():
            (latc, longc) = (lat+(width/2), lon+(height/2))
            radius = (height/2)*69.09
            self.threadPool.append(MyThread(self.rest.getTweetsInsideArea, latc, longc, radius))
        self.streaming.trackTweetsInsideArea(lat1, lon1, lat2, lon2)
        
    def trackTweetsByContent(self, content):
        if self.rest.isEnabled():
            self.threadPool.append(MyThread(self.rest.getTweetsByContent, content))
        self.streaming.trackTweetsByContent(content)

        
    def stop(self):
        self.streaming.stop()