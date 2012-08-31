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

import sys, os.path, datetime
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from PySide.QtOpenGL import *
from backend.Base import *
from threading import Timer

from backend.Crawler import *

class Controller(Crawler):
    def __init__(self):
        Crawler.__init__(self)
        self.last_id = 0
        self._tweets = []
        self.lastSearch = None
        self.resetTimer = Timer(500.0, self.restartLastSearch)
    
    def getAuthUrl(self):
        return Crawler.getAuthUrl(self)
    
    def login(self):
        return Crawler.login(self)
    
    @Slot("QVariant")
    def updateSearchStep(self, step):
        Crawler.updateSearchStep(self, step)
        for tweet in step:
            self._tweets.append(tweet)
        self.tweetsUpdated.emit()
        
    @Slot(str)
    def loginWithCode(self, code):
        self.setAuthAccess(code)
        self.login()
    
    @Slot()    
    def createNewSearch(self):
        self.db.deleteAll()
    
    @Slot()
    def stop(self):
        Crawler.stop(self)
    
    @Slot(float, float, float, float)    
    def startRealtimeMapSearch(self, lat1, lon1, lat2, lon2):
        self.getTweetsInsideArea(lat1, lon1, lat2, lon2, crawler=STREAMING_CRAWLER)
        
    @Slot(float, float, float, float, int)
    def startHistoricalMapSearch(self, lat1, lon1, lat2, lon2, delta, page=1):
        self.lastSearch = {"type": "historicalMap", "lat1": lat1, "lon1": lon1, "lat2": lat2, "lon2": lon2, "delta": delta, "page": page}
        today = datetime.datetime.today().date()
        until = today - datetime.timedelta(days=delta)
        untilstr = until.strftime("%Y-%m-%d")
        self.getTweetsInsideArea(lat1, lon1, lat2, lon2, crawler=REST_CRAWLER, until=untilstr, page=page)
    
    @Slot(str)
    def startRealtimeContentSearch(self, content):
        self.lastSearch = {"type": "realtimeContent", "content": content}
        self.getTweetsByContent(content, crawler=STREAMING_CRAWLER)
    
    @Slot(str, int)    
    def startHistoricalContentSearch(self, content, delta, page=1):
        self.lastSearch = {"type": "historicalContent", "content": content, "delta": delta, "page": page}
        today = datetime.datetime.today().date()
        until = today - datetime.timedelta(days=delta)
        untilstr = until.strftime("%Y-%m-%d")
        self.getTweetsByContent(content, crawler=REST_CRAWLER, until=untilstr, page=page)
        
    @Slot(str)
    def startHistoricalUserSearch(self, username):
        self.getTweetsByUser(username, crawler=REST_CRAWLER)
    
    @Slot()    
    def getMoreHistoricalResults(self):
        if self.lastSearch["type"] == "historicalContent":
            self.startHistoricalContentSearch(self.lastSearch["content"], 
                                              self.lastSearch["delta"], 
                                              self.lastSearch["page"]+1)
        elif self.lastSearch["type"] == "historicalMap":
            self.startHistoricalMapSearch(self.lastSearch["lat1"],
                                          self.lastSearch["lon1"], 
                                          self.lastSearch["lat2"],
                                          self.lastSearch["lon2"], 
                                          self.lastSearch["delta"], 
                                          self.lastSearch["page"]+1)
        
    @Slot(int)
    def errorHandler(self, code):
        Crawler.errorHandler(self, code)
        try:
            self.resetTimer.start()
        except RuntimeError as e:
            return
        
    def restartLastSearch(self):
        if self.lastSearch == None:
            return
        if self.lastSearch["type"] == "realtimeContent":
            self.startRealtimeContentSearch(self.lastSearch["content"])
        elif self.lastSearch["type"] == "historicalContent":
            self.startHistoricalContentSearch(self.lastSearch["content"], self.lastSearch["delta"])
    
    def getTweets(self):
        tweets = self._tweets
        self._tweets = []
        return tweets
    
    @Slot(str)
    def getUserTweets(self, userName):
        res = []
        for tid in self.db.getUserTweets(userName):
            res.append(tid[0])
        print res
        self.userTracked.emit(res)
        
    
    changed = Signal()
    loginChanged = Signal()
    tweetsUpdated = Signal()
    userTracked = Signal("QVariant")
    loginUrl = Property(unicode, getAuthUrl, notify=loginChanged)
    loggedIn = Property(bool, login, notify=changed)
    tweets = Property("QVariant", getTweets, notify=tweetsUpdated)
    

if __name__ == "__main__":
    frontend = os.path.join(os.path.realpath(os.path.dirname(__file__)), "frontend")
    app = QApplication(sys.argv)
    qmlRegisterType(Controller, "TwitterCrawler", 1, 0, "Controller")
    
    view = QDeclarativeView()
    view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
    root = view.rootContext()

    view.setSource(os.path.join(frontend, "frontend.qml")) 
    view.show()
    
    app.exec_()
    sys.exit()               