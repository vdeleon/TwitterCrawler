'''
Created on 09/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
from PySide.QtCore import *

class User(object):
    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id
        self.db_id = None
        self.followers = []
        
class Tweet(object):
    def __init__(self, user=None, time=None, location=None, hashtags = [], links = []):
        self.user = user
        self.time = time
        self.location = location
        self.hashtags = hashtags
        self.links = links
        
class SearchStep(object):
    def __init__(self, users=[], tweets=[]):
        self.users = users
        self.tweets = tweets

class MyThread(QThread):
    def __init__(self, method, *args):
        QThread.__init__(self)
        self.method = method
        self.args = args
        self.start()
        
    def run(self):
        self.method(*self.args)
        
class SearchSignal(QObject):
    dataReady = Signal(SearchStep)