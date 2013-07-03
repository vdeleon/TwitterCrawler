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
    '''
    Abstract crawler structure
    '''
    cron = None
    """
    @var cron: action's history
    @type: History
    """
    
    allowed_param = []
    """
    @var allowed_param: list of allowed parameters
    @type: array
    """
    
    def __init__(self, allowed_param=[], enable_history=True):
        self.allowed_param=allowed_param
        if enable_history:
            self.cron = History()
        
    def __crawlAction(self, function, *args, **parameters):
        keys = parameters.keys()
        if self.allowed_param != []:
            for k in keys:
                if k not in self.allowed_param:
                    raise ArgumentException("wrong parameter on crawling function")
        if self.cron != None:
            return self.cron.add([function, args, parameters])
            
    def setMaxId(self, index, max_id):
        if self.cron == None:
            return
        self.cron.actions[index][2]["max_id"] = max_id
    
    def getTweetsInsideArea(self, lat1, lon1, lat2, lon2, **parameters):
        """
        Get every tweet from a given location
        """
        return self.__crawlAction(self.getTweetsInsideArea, lat1, lon1, lat2, lon2, **parameters)
    
    def getTweetsByContent(self, content, **parameters):
        """
        Get tweets that contains a given content
        """
        return self.__crawlAction(self.getTweetsByContent, content, **parameters)
    
    def getTweetsByUser(self, username, **parameters):
        """
        Get tweets from a given user timeline
        """
        return self.__crawlAction(self.getTweetsByUser, username, **parameters)