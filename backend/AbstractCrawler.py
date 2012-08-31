'''
Created on 26/giu/2012

@author: riccardo
'''

class AbstractCrawler(object):
    '''
    Abstract crawler structure
    '''
    def __init__(self, allowed_param=[]):
        self.allowed_param=allowed_param
        
    def checkParameters(self, **parameters):
        keys = parameters.keys()
        for k in keys:
            if k not in self.allowed_param:
                return False
        return True
    
    def getTweetsInsideArea(self, lat1, lon1, lat2, lon2, **parameters):
        '''
        Get every tweet from a given location
        '''
        raise NotImplementedError()
    
    def getTweetsByContent(self, content, **parameters):
        '''
        Get tweets that contains a given content
        '''
        raise NotImplementedError()
    
    def getTweetsByUser(self, username, **parameters):
        raise NotImplementedError()