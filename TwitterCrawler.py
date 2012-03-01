'''
Created on 15/feb/2012

@author: riccardo
'''
from urllib2 import *
import sys, json
from urllib import urlencode

class TwitterCrawler():
    def __init(self):
        pass
    
    def __restCommand(self, url, params):
        req = Request(url, urlencode(params))
        data = urlopen(req).read()
        print data
        return json.loads(data)
    
    def getUserId(self, username):
        params = {'screen_name': username}
        jdata = self.__restCommand("https://api.twitter.com/1/users/lookup.json", params)
        return jdata[0]["id"]
    
    def getUserTweet(self, userid):
        params = {'user_id': userid, "include_entities": 1, "exclude_replies": 1}
        jdata = self.__restCommand("https://api.twitter.com/1/statuses/user_timeline.json", params)
        
if __name__ == "__main__":
    crawler = TwitterCrawler()
    crawler.getUserTweet(190168868)
        
