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
from PySide.QtCore import *
from Base import *
from time import time
import pprint as p

class Listener(QObject, streaming.StreamListener):
    
    streamingDataReady = Signal("QVariant")
    
    def __init__(self, api=None, parent=None):
        QObject.__init__(self, parent)
        streaming.StreamListener.__init__(self, api)
        
    def on_status(self, status):
        try:
            step = {"users": [], "tweets": []}
            step["tweets"].append({"userId": status.user.id, 
                                   "userName": status.user.screen_name,
                                   "time":  int(time()),
                                   "location": (status.place["bounding_box"]["coordinates"][0][0][1], status.place["bounding_box"]["coordinates"][0][0][0]),
                                   "hashtags": [],
                                   "links": []})
            for h in status.entities["hashtags"]:
                step["tweets"][-1]["hashtags"].append(h["text"])
            for u in status.entities["urls"]:
                step["tweets"][-1]["links"].append(u["expanded_url"])
            self.streamingDataReady.emit(step)
        except Exception:
            return
        
    def on_error(self, status_code):
        print status_code
        
class StreamingCrawler(QObject):
    def __init__(self, auth):
        QObject.__init__(self)
        self.signal = SearchSignal()
        if auth == None:
            raise ValueError("auth is not valid!")
        self.listener = Listener()
        self.stream = streaming.Stream(auth, self.listener)
        
    def trackTweetsInsideArea(self, lat1, lon1, lat2, lon2):
        self.stream.filter(locations=(lon1, lat2, lon2, lat1), async=True)
        
    def trackTweetsByContent(self, content):
        print content
        self.stream.filter(track=[content], async=True)
            
    def stop(self):
        self.stream.disconnect()