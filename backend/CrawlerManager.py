'''
Created on 05/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
from RestCrawler import *
from StreamingCrawler import *

class CrawlerManager(object):
    def __init__(self):
        self.rest = RestCrawler()
        self.streaming = StreamingCrawler()