'''
Created on 05/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
from tweepy import API as rest
from Base import *
from PySide.QtCore import *
from tweepy.models import SearchResult

class RestCrawler(QObject):
    def __init__(self, auth=None):
        QObject.__init__(self, None)
        self.__enabled = True
        self.rest = rest(auth)
        self.dataReady = Signal(SearchStep)
    
    def disable(self):
        self.__enabled = False
        
    def isEnabled(self):
        return self.__enabled
    
    def enable(self):
        self.__enabled = True
        
    def getPlaceCoordinates(self, name):
        self.rest.geo_search(query=name)
        '''TODO: get search result'''
        pass
    
    def getTweetsInsideArea(self, lat, long, radius):
        string = "%f,%f,%fmi" % (lat, long, radius)
        results = self.rest.search(geocode=string, include_entities=True)
        sStep = SearchStep()
        for res in results:
            if res.geo == None:
                (tlat, tlong) = self.getPlaceCoordinates(res.location)
            else:
                (tlat, tlong) = res.geo["coordinates"]
            tweet = Tweet(user=User(res.from_user, res.from_user_id), time=res.created_at, location=(tlat, tlong))
            for u in res.entities["urls"]:
                tweet.links.append(u["expanded_url"])
            for h in res.entities["hashtags"]:
                tweet.hashtags.append(h["text"])
            sStep.tweets.append(tweet)
        self.dataReady.emit(sStep)
        
    def getUserFollowers(self, user):
        result = self.rest.followers(user.id)
        sStep = SearchStep()
        for res in result:
            user.followers.append(User(name=user.screen_name, id=res.id))
            sStep.users.append(user)
        self.dataReady.emit(sStep)
        
if __name__ == "__main__":
    import pprint as p
    crawler = RestCrawler()
    string = "%f,%f,%fmi" % (45.6426657, 12.623754, 5)
    res = crawler.rest.search(geocode=string, include_entities=True)
    for r in res:
        p.pprint(r.__getstate__())
    