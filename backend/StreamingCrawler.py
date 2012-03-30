'''
Created on 05/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import tweepy.streaming as streaming
from PySide.QtCore import *
from Base import *
from time import time
import pprint as p

class Listener(QObject, streaming.StreamListener):
    def __init__(self, api=None, parent=None):
        QObject.__init__(self, parent)
        streaming.StreamListener.__init__(self, api)
        self.signal = SearchSignal()
        
    def on_status(self, status):
        sStep = SearchStep()
        tweet = Tweet(user=User(status.user.screen_name, status.user.id), 
                      time=int(time()), 
                      location=(status.place["bounding_box"]["coordinates"][0][0][1], status.place["bounding_box"]["coordinates"][0][0][0]))
        for h in status.entities["hashtags"]:
            tweet.hashtags.append(h["text"])
        for u in status.entities["urls"]:
            tweet.links.append(u["expanded_url"])
        sStep.tweets.append(tweet)
        self.signal.dataReady.emit(sStep)
        
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
        self.listener.signal.dataReady.connect(self.getRealtimeData)
        
    def trackTweetsInsideArea(self, lat1, lon1, lat2, lon2):
        self.stream.filter(locations=(lon1, lat2, lon2, lat1), async=True)
    
    @Slot(SearchStep)    
    def getRealtimeData(self, step):
        self.signal.dataReady.emit(step)
        
    def stop(self):
        self.stream.disconnect()