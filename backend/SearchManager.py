'''
Created on 10/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
from PySide.QtCore import *
from Crawler import Crawler
from Database import *
from Base import *

class SearchManager(QObject):
    def __init__(self):
        self.search = None
        self.step = 0
        self.db = DatabaseManager()
        self.crawler = Crawler()
    
    def createSearch(self):
        self.search = self.db.createSearch("Temp")
        
    def addSearchStep(self):
        self.db.addSearchStep(self.search)
    
    @Slot(SearchStep)
    def mergeStep(self, step):
        for u in step.users:
            self.db.addUser(u.id, u.name, self.search, self.step)
            for f in u.followers:
                self.db.addFollower(f.id, f.name, self.search, self.step, self.db.getUserId(t_screen_name=u.name))
        for t in step.tweets:
            self.db.addUser(t.user.id, t.user.name, self.search, self.step)
            userId = self.db.getUserId(t_screen_name=t.user.name)
            if t.location != None:
                self.db.addLocation(userId, t.time, t.location[0], t.location[1])
            for tag in t.hashtags:
                self.db.addHashtag(userId, tag)
            for link in t.links:
                self.db.addLink(userId, link)