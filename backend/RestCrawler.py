'''
Created on 05/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import tweepy.API as rest

class RestCrawler(object):
    def __init__(self, auth=None):
        self.__enabled = True
        pass
    
    def disable(self):
        self.__enabled = False
        
    def isEnabled(self):
        return self.__enabled
    
    def enable(self):
        self.__enabled = True
        