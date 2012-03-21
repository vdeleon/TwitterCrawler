'''
Created on 05/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
from tweepy import API as rest
from tweepy.error import *
from Base import *
from PySide.QtCore import *

class RestCrawler(QObject):
    
    dataReady = Signal(SearchStep)
    
    def __init__(self, auth=None):
        QObject.__init__(self)
        self.__enabled = True
        self.rest = rest(auth)
        #self.signal = SearchSignal()
        self.known_locations = {}
    
    def disable(self):
        self.__enabled = False
        
    def isEnabled(self):
        return self.__enabled
    
    def enable(self):
        self.__enabled = True
        
    def getPlaceCoordinates(self, name):
        if name in self.known_locations:
            return self.known_locations[name]
        try:
            results = self.rest.geo_search(query=name)
            coordinates = None
            if len(results["result"]["places"]) == 0:
                coordinates = (None, None)
            for place in results["result"]["places"]:
                if place["name"] == name:
                    coordinates = place["bounding_box"]["coordinates"][0][0]
            if coordinates == None:
                coordinates = results["result"]["places"][0]["bounding_box"]["coordinates"][0][0]
            self.known_locations[name] = (coordinates[1], coordinates[0])
            return (coordinates[1], coordinates[0])
        except TweepError as e:
            print e.resp
            return (None, None)
    
    @Slot(float, float, float)
    def getTweetsInsideArea(self, lat, long, radius):
        print QThread.currentThread()
        string = "%f,%f,%fmi" % (lat, long, radius)
        results = self.rest.search(geocode=string, include_entities=True, rpp=100)
        sStep = SearchStep()
        for res in results:
            if res.geo == None:
                (tlat, tlong) = self.getPlaceCoordinates(res.location)
            else:
                (tlat, tlong) = res.geo["coordinates"]
            if tlat == None:
                continue;
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
    #res = crawler.rest.search(geocode=string, include_entities=True)
    res = crawler.rest.geo_search(query="Treviso")
    
    print res["result"]["places"]
    print res["result"]["places"][0]["bounding_box"]["coordinates"][0][0]
    #p.pprint(res.__getstate__())
    