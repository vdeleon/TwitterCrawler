'''
Created on 05/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
from RestCrawler import *
from StreamingCrawler import *
import tweepy
from backend.StreamingCrawler import StreamingCrawler

class CrawlerManager(object):
    def __init__(self):
        self.rest = None
        self.streaming = None
        self.auth = None
        self.setCrawlers()
        
    def LoginBasic(self, username, password):
        self.auth = tweepy.BasicAuthHandler(username, password)
        self.setCrawlers()
    
    def LoginOauth(self):
        pass
    
    def setCrawlers(self):
        self.rest = RestCrawler(self.auth)
        self.streaming = StreamingCrawler(self.auth)