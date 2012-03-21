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

class Crawler(QObject):
    
    dataReady = Signal(SearchStep)
    
    def __init__(self):
        QObject.__init__(self)
        self.rest = None
        self.restThread = MyThread()
        self.streaming = None
        self.auth = None
        self.settings = QSettings("rferrazz", "TwitterCrawler")
        #self.signal = SearchSignal()
        
    def authInit(self):
        self.rest = RestCrawler(self.auth)
        self.rest.moveToThread(self.restThread)
        self.restThread.start()
        self.streaming = StreamingCrawler(self.auth)
        self.rest.dataReady.connect(self.saveResults)
        QObject.connect(self.streaming, SIGNAL('dataReady(object)'), self.saveResults)
        
    @Slot(SearchStep)
    def saveResults(self, step):
        self.dataReady.emit(step)
    
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
            print QThread.currentThread()
            self.restThread.getTweetsInsideArea(latc, longc, radius)
        self.streaming.trackTweetsInsideArea(lat1, lon1, lat2, lon2)