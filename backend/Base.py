'''
Copyright (C) 2012 Riccardo Ferrazzo <f.riccardo87@gmail.com>

This file is part of TwitterCrawler.

    TwitterCrawler is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TwitterCrawler is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with TwitterCrawler.  If not, see <http://www.gnu.org/licenses/>
    
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
        QObject.__init__(self)
        self.users = users
        self.tweets = tweets

class MyThread(QThread):
    def __init__(self, method, *args, **kwargs):
        QThread.__init__(self)
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.start()
        
    def run(self):
        self.method(*self.args, **self.kwargs)
        
class SearchSignal(QObject):
    dataReady = Signal(SearchStep)