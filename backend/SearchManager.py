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
        self.crawler = Crawler(self.db)
    
    def createSearch(self):
        self.search = Search()
        self.step = 0
        
    def addSearchStep(self):
        self.search.addStep()
    
    @Slot(SearchStep)
    def mergeStep(self, step):
        for u in step.users:
            self.search.steps[step].users.append(u)
        for t in step.tweets:
            self.search.steps[step].tweets.append(t)
            
    def saveCurrentSearch(self, name):
        pass