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
import tweepy.streaming as streaming
import datetime
from PySide.QtCore import *
from Base import *
from AbstractCrawler import AbstractCrawler

class SecureStream(streaming.Stream):
    def __init__(self, auth, listener, **options):
        streaming.Stream.__init__(self, auth, listener, **options)
        
    def on_closed(self, resp):
        self.listener.streamingError.emit(599)
        

class Listener(QObject, streaming.StreamListener):
    
    streamingDataReady = Signal("QVariant")
    streamingError = Signal(int)
    
    def __init__(self, api=None, parent=None):
        QObject.__init__(self, parent)
        streaming.StreamListener.__init__(self, api)
        
    def on_limit(self, track):
        self.streamingError.emit(604)
    
    def on_timeout(self):
        print "timeout"
        
    def on_status(self, status):
        try:
            step = []
            time = datetime.datetime.now()
            step.append({"userId": status.user.id, 
                         "userName": status.user.screen_name,
                         "year": time.year,
                         "month": time.month,
                         "day": time.day,
                         "hour": time.hour,
                         "minute": time.minute,
                         "second": time.second,
                         "location": False,
                         "tweet": status.text,
                         "hashtags": [],
                         "links": []})
            if status.geo != None:
                step[-1]["location"] = {"lat":status.geo["coordinates"][0], "lon":status.geo["coordinates"][1]}
            elif status.coordinates != None:
                step[-1]["location"] = {"lat":status.coordinates["coordinates"][1], "lon": status.coordinates["coordinates"][0]}
            elif status.place != None: #More generic
                step[-1]["location"] = {"lat": status.place["bounding_box"]["coordinates"][0][0][1], "lon": status.place["bounding_box"]["coordinates"][0][0][0]}
            for h in status.entities["hashtags"]:
                step[-1]["hashtags"].append(h["text"])
            for u in status.entities["urls"]:
                step[-1]["links"].append(u["expanded_url"])
            self.streamingDataReady.emit(step)
        except Exception as e:
            print e
            self.streamingError.emit(600)
        
    def on_error(self, status_code):
        self.streamingError.emit(status_code)
        
class StreamingCrawler(AbstractCrawler):
    def __init__(self, auth, headers={}):
        AbstractCrawler.__init__(self, allowed_param=[], enable_history=False)
        self.threadPool = []
        if auth == None:
            raise ValueError("auth is not valid!")
        self.listener = Listener()
        self.stream = SecureStream(auth, self.listener, headers=headers, retry_count=10)
        
    def getTweetsInsideArea(self, lat1, lon1, lat2, lon2, **parameters):
        AbstractCrawler.getTweetsInsideArea(self, lat1, lon1, lat2, lon2, **parameters)
        self.threadPool.append(MyThread(self.stream.filter, locations=(lon1, lat2, lon2, lat1)))
        
    def getTweetsByContent(self, content, **parameters):
        AbstractCrawler.getTweetsByContent(self, content, **parameters)
        self.threadPool.append(MyThread(self.stream.filter, track=[content]))
            
    def stop(self):
        removable = []
        self.stream.disconnect()
        for i in range(len(self.threadPool)):
            if not self.threadPool[i].isRunning():
                removable.append(i)
        for i in removable:
            self.threadPool.pop(i)
            