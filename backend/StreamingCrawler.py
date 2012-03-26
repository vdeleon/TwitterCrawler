'''
Created on 05/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import tweepy.streaming as streaming
from PySide.QtCore import *
from Base import *

class Listener(streaming.StreamListener, QObject):
    def __init__(self):
        QObject.__init__(self)
        self.signal = SearchSignal()
        
    def on_status(self, status):
        sStep = None
        self.signal.dataReady.emit(sStep)

class StreamingCrawler(QObject):
    def __init__(self, auth, listener):
        QObject.__init__(self)
        self.dataReady = Signal(SearchStep)
        if auth == None:
            raise ValueError("auth is not valid!")
        self.listener = listener
        self.stream = streaming.Stream(auth, self.listener)
        
    def trackTweetsInsideArea(self, lat1, lon1, lat2, lon2):
        self.stream.filter(locations=(lat1, lon1, lat2, lon2))
        
    @Slot()
    def stop(self):
        self.stream.disconnect()