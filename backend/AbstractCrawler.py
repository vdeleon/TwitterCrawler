'''
Created on 26/giu/2012

@author: riccardo
'''

class ArgumentException(Exception):
    def __init__(self, message):
        self.message = "Argument Error: %s", (message,)
        
class HistoryException(Exception):
    def __init__(self, name):
        self.message = "History error: %s not found" % (name,)

class History(object):
    
    actions = []
        
    def __search(self, name, *args):
        for i in range(len(self.actions)-1, -1, -1):
            if self.actions[i][0].__name__ == name:
                for a in args:
                    if a not in self.actions[i][1]:
                        print "arg not found"
                        raise HistoryException(name)
                return i
        raise HistoryException(name)
        
    def add(self, action):
        self.actions.append(action)
        return len(self.actions)-1
        
    def repeatLast(self, name="", *args):
        fun, args, kwargs = self.getLast(name, *args)
        return fun(*args, **kwargs)
    
    def getLast(self, name="", *args):
        last = -1
        if name != "":
            last = self.__search(name, *args)
        return self.actions[last]
        
class AbstractCrawler(object):
    
    def __init__(self, allowed_param=[]):
        self.allowed_param=allowed_param
        self.cron = History()
          
    @classmethod
    def traceHistory(klass, fun):
        def _traceHistory(*args, **kwargs):
            args[0].cron.add([fun, args, kwargs])
            fun(*args, **kwargs)
        return _traceHistory
               
    @classmethod
    def crawlingAction(klass, fun):
        def _crawlingAction(self, *args, **kwargs):
            keys = kwargs.keys()
            if self.allowed_param != []:
                for k in keys:
                    if k not in self.allowed_param:
                        raise ArgumentException("wrong parameter on crawling function")
            #function
            fun(self, *args, **kwargs)
        return _crawlingAction
        
    def getTweetsInsideArea(self, lat1, lon1, lat2, lon2, **parameters):
        """
        Get every tweet from a given location
        """
        raise NotImplementedError()
    
    def getTweetsByContent(self, content, **parameters):
        """
        Get tweets that contains a given content
        """
        raise NotImplementedError()
    
    def getTweetsByUser(self, username, **parameters):
        """
        Get tweets from a given user timeline
        """
        raise NotImplementedError()