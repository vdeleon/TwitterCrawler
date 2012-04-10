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
from tweepy import API as rest
from tweepy.error import *
from Base import *
from PySide.QtCore import *

class RestCrawler(QObject):
    
    restDataReady = Signal(SearchStep)
    
    def __init__(self, auth=None, parent=None):
        QObject.__init__(self, parent)
        self._enabled = True
        self.rest = rest(auth)
        self.known_locations = {}
    
    def disable(self):
        self._enabled = False
        
    def isEnabled(self):
        return self._enabled
    
    def enable(self):
        self._enabled = True
        
    def getPlaceCoordinates(self, name):
        if name in self.known_locations:
            return self.known_locations[name]
        try:
            results = self.rest.geo_search(query=name)
            coordinates = None
            if len(results["result"]["places"]) == 0:
                coordinates = (False, False)
            for place in results["result"]["places"]:
                if place["name"] == name:
                    coordinates = place["bounding_box"]["coordinates"][0][0]
            if coordinates == None and results["result"]["places"][0]["bounding_box"]["coordinates"][0][0] != None:
                coordinates = results["result"]["places"][0]["bounding_box"]["coordinates"][0][0]
            self.known_locations[name] = (coordinates[1], coordinates[0])
            return (coordinates[1], coordinates[0])
        except TweepError as e:
            return (False, False)
    
    def getTweetsInsideArea(self, lat, long, radius):
        string = "%f,%f,%fmi" % (lat, long, radius)
        try:
            results = self.rest.search(geocode=string, include_entities=True, rpp=100, result_type="recent")
        except Exception:
            '''sometimes tweepy fails'''
            return
        step = {"users": [], "tweets": []}
        for res in results:
            if res.geo == None:
                (tlat, tlong) = self.getPlaceCoordinates(res.location)
            else:
                (tlat, tlong) = res.geo["coordinates"]
            if tlat == False:
                continue;
            step["tweets"].append({"userId": res.from_user_id,
                                   "userName": res.from_user,
                                   "time": int(res.created_at.strftime("%s")),
                                   "location": (tlat, tlong),
                                   "hashtags": [],
                                   "links": []})
            for u in res.entities["urls"]:
                step["tweets"][-1]["links"].append(u["expanded_url"])
            for h in res.entities["hashtags"]:
                step["tweets"][-1]["hashtags"].append(h["text"])
        self.restDataReady.emit(step)
        
    def getUserFollowers(self, user):
        result = self.rest.followers(user.id)
        sStep = SearchStep()
        for res in result:
            user.followers.append(User(name=user.screen_name, id=res.id))
            sStep.users.append(user)
        self.restDataReady.emit(sStep)
        
    def getTweetsByContent(self, content):
        pass
        
if __name__ == "__main__":
    import pprint as p
    crawler = RestCrawler()
    string = "%f,%f,%fmi" % (45.6426657, 12.623754, 5)
    #res = crawler.rest.search(geocode=string, include_entities=True)
    res = crawler.rest.geo_search(query="Treviso")
    
    print res["result"]["places"]
    print res["result"]["places"][0]["bounding_box"]["coordinates"][0][0]
    #p.pprint(res.__getstate__())
    