'''
Created on 05/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import tweepy.API as rest
from PySide.QtCore import *

class RestCrawler(QObject):
    def __init__(self, auth=None):
        self.__enabled = True
        self.rest = rest(auth)
        self.resultsReady = Signal(list)
        pass
    
    def disable(self):
        self.__enabled = False
        
    def isEnabled(self):
        return self.__enabled
    
    def enable(self):
        self.__enabled = True
        
    def parseResults(self, results):
        '''emit a signal with correct results'''
        parsed = []
        for res in results:
            dict = {"t_id": res.from_user_id, "t_screen_name": res.from_user, "location": res.location, "time": res.created_at,  "links": [], "hashtags": []}
            for u in res.entities["urls"]:
                res["links"] = u["expanded_url"]
            for h in res.entities["hashtags"]:
                res["hashtags"] = h["text"]
            parsed.append(dict)
        self.resultsReady.emit(parsed)
            
    
    def getTweetsInsideArea(self, lat, long, radius):
        string = "%f,%f,%fmi" % (lat, long, radius)
        results = self.rest.search(geocode=string, include_entities=True)
        self.parseResults(results)    