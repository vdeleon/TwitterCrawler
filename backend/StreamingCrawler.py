'''
Created on 05/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import tweepy.streaming as streaming

class Listener(streaming.StreamListener):
    def on_status(self, status):
        pass

class StreamingCrawler(object):
    def __init__(self, auth):
        if auth == None:
            raise ValueError("auth is not valid!")
        self.listener = Listener()
        self.stream = streaming.Stream(auth, self.listener)
        
    def trackTweetsInsideArea(self, lat1, lon1, lat2, lon2):
        self.stream.filter(locations=(lat1, lon1, lat2, lon2))