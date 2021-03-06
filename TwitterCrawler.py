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
from backend.AbstractCrawler import HistoryException
from PySide import QtGui

class Controller(Crawler):
    def __init__(self):
        Crawler.__init__(self)
        self.last_id = 0
        self._tweets = []
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
        
    @Slot("QVariant")
    def saveSearch(self, ids):
        outputFile = QFileDialog.getSaveFileName(caption="Save File")
        if outputFile == '':
            return
        if ids != 0:
            fd = open(outputFile[0], "w")
            for name in ids:
                tweets = self.db.getUserTweetsComplete(name)
                fd.write("%s,lat,lon\n" % (",".join(tweets[0].keys())))
                for tweet in tweets:
                    coordinates = self.db.getIdLocation(tweet["id"])
                    converter = (type(w).__name__ in ['str', 'unicode'] and u'"'+w+u'"' or unicode(w) for w in tweet)
                    fd.write(",".join(converter))
                    fd.write(",%s,%s\n" % (coordinates["lat"], coordinates["lon"]))
            fd.close()
        else:
            self.export(outputFile[0])
    
    @Slot(float, float, float, float)    
    def startRealtimeMapSearch(self, lat1, lon1, lat2, lon2):
        self.getTweetsInsideArea(lat1, lon1, lat2, lon2, crawler=STREAMING_CRAWLER)
        
    @Slot(float, float, float, float, int)
    def startHistoricalMapSearch(self, lat1, lon1, lat2, lon2, delta, max_id=-1):
        today = datetime.datetime.today().date()
        until = today - datetime.timedelta(days=delta)
        untilstr = until.strftime("%Y-%m-%d")
        self.getTweetsInsideArea(lat1, lon1, lat2, lon2, crawler=REST_CRAWLER, until=untilstr, max_id=max_id)
    
    @Slot(str)
    def startRealtimeContentSearch(self, content):
        self.getTweetsByContent(content, crawler=STREAMING_CRAWLER)
    
    @Slot(str, int)    
    def startHistoricalContentSearch(self, content, delta, max_id=-1):
        today = datetime.datetime.today().date()
        until = today - datetime.timedelta(days=delta)
        untilstr = until.strftime("%Y-%m-%d")
        self.getTweetsByContent(content, crawler=REST_CRAWLER, until=untilstr, max_id=max_id)
        
    @Slot(str)
    def startHistoricalUserSearch(self, username, max_id=-1):
        try:
            fun, args, kwargs = self.cron.getLast("getTweetsByUser", username)
            kwargs["max_id"] = self.max_id + 1
            return fun(*args, **kwargs)
        except HistoryException:
            return self.getTweetsByUser(username, crawler=REST_CRAWLER, max_id=max_id)
    
    @Slot()    
    def getMoreHistoricalResults(self):
        fun, args, kwargs = self.cron.getLast()
        kwargs["max_id"] = self.max_id+1
        print args, kwargs
        fun(*args, **kwargs)
        
    @Slot(int)
    def errorHandler(self, code):
        Crawler.errorHandler(self, code)
        try:
            self.resetTimer.start()
        except RuntimeError as e:
            return
        
    def restartLastSearch(self):
        self.cron.repeatLast()
    
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