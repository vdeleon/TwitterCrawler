'''
Created on 09/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''

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