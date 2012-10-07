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
from AbstractCrawler import AbstractCrawler
from PySide.QtCore import *

class RestCrawler(QObject, AbstractCrawler):
    
    restDataReady = Signal("QVariant")
    
    def __init__(self, auth=None, parent=None):
        QObject.__init__(self, parent)
        AbstractCrawler.__init__(self, allowed_param=["until", "page"], enable_history=False)
        self.rest = rest(auth)
        self.known_locations = {}
        
    def generateSearchStep(self, results, user=False):
        step = []
        for res in results:
            step.append({"year": res.created_at.year,
                         "month": res.created_at.month,
                         "day": res.created_at.day,
                         "hour": res.created_at.hour,
                         "minute": res.created_at.minute,
                         "second": res.created_at.second,
                         "location": False,
                         "tweet": res.text,
                         "hashtags": [],
                         "links": []})
            if user:
                step[-1]["userId"] = res.user.id
                step[-1]["userName"] = res.user.screen_name
            else:
                step[-1]["userId"] = res.from_user_id
                step[-1]["userName"] = res.from_user
            if res.geo == None:
                try:
                    (tlat, tlong) = self.getPlaceCoordinates(res.location)
                except AttributeError as e:
                    (tlat, tlong) = (False, False)
            else:
                (tlat, tlong) = res.geo["coordinates"]
            if tlat != False:
                step[-1]["location"] = {"lat":tlat, "lon":tlong}
            for u in res.entities["urls"]:
                step[-1]["links"].append(u["expanded_url"])
            for h in res.entities["hashtags"]:
                step[-1]["hashtags"].append(h["text"])
        return step
        
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
    
    def getTweetsInsideArea(self, lat1, lon1, lat2, lon2, **parameters):
        AbstractCrawler.getTweetsInsideArea(self, lat1, lon1, lat2, lon2, **parameters)
        width = abs(lat2-lat1)
        height = abs(lon2-lon1)
        if lat1 < lat2:
            lat = lat1
        else:
            lat = lat2
        if lon1 < lon2:
            lon = lon1
        else:
            lon = lon2
        (latc, longc) = (lat+(width/2), lon+(height/2))
        radius = (height/2)*69.09
        string = "%f,%f,%fmi" % (latc, longc, radius)
        try:
            results = self.rest.search(geocode=string, include_entities=True, rpp=100, result_type="recent", **parameters)
            self.restDataReady.emit(self.generateSearchStep(results))
        except Exception as e:
            raise e 
        
#    def getUserFollowers(self, user):
#        result = self.rest.followers(user.id)
#        sStep = SearchStep()
#        for res in result:
#            user.followers.append(User(name=user.screen_name, id=res.id))
#            sStep.users.append(user)
#        self.restDataReady.emit(sStep)
        
    def getTweetsByContent(self, content, **parameters):
        AbstractCrawler.getTweetsByContent(self, content, **parameters)
        results = self.rest.search(q=content, include_entities=True, rpp=100, **parameters)
        self.restDataReady.emit(self.generateSearchStep(results))
        
    def getTweetsByUser(self, username, **parameters):
        AbstractCrawler.getTweetsByUser(self, username, **parameters)
        results = self.rest.user_timeline(screen_name=username, include_entities=True, **parameters)
        self.restDataReady.emit(self.generateSearchStep(results, True))
    