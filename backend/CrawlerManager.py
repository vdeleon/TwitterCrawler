'''
Created on 05/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
from RestCrawler import *
from StreamingCrawler import *
from Database import *
from PySide.QtCore import *
import tweepy

CONSUMER_KEY = ""
CONSUMER_SECRET = ""

class CrawlerManager(QObject):
    def __init__(self):
        self.rest = None
        self.streaming = None
        self.auth = None
        self.db = DatabaseManager()
    
    def getAuthUrl(self):
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        return self.auth.get_authorization_url()
    
    def setAuthAccess(self, verifier):
        self.auth.get_access_token(verifier)
        self.db.addOption("auth_key", self.auth.access_token.key)
        self.db.addOption("auth_secret", self.auth.access_token.secret)
            
    def login(self):
        try:
            key = self.db.getOption("auth_key")
            secret = self.db.getOption("auth_secret")
        except Exception:
            return False
        if self.auth == None:
            self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(key, secret)
        self.rest = RestCrawler(self.auth)
        self.streaming = StreamingCrawler(self.auth)
        return True
    
    def saveResults(self, results):
        '''slot called when results are ready to save'''
        pass
    
    def trackTweetsInsideArea(self, lat, long, width, height):
        '''Get tweets inside the given bounding box'''
        if self.rest.isEnabled():
            (latc, longc) = (lat+(width/2), long+(height/2))
            radius = (height/2)*69.09
            self.rest.getTweetsInsideArea(latc, longc, radius)
        self.streaming.trackTweetsInsideArea(lat, long, width, height)