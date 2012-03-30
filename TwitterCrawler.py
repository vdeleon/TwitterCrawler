'''
Created on 15/feb/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import sys, os.path
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from PySide.QtOpenGL import *
from backend.Base import *

from backend.Crawler import Crawler

class Controller(Crawler):
    def __init__(self):
        Crawler.__init__(self)
        self.last_id = 0
        self._locations = []
        self._pointsInfo = {}
    
    def getSearch(self):
        if self.search != None:
            return "Temp"
        return "None"
    
    def getAuthUrl(self):
        return Crawler.getAuthUrl(self)
    
    def login(self):
        return Crawler.login(self)
    
    def getSteps(self):
        return str(Crawler.getSteps(self))
    
    @Slot(SearchStep)
    def updateSearchStep(self, step):
        Crawler.updateSearchStep(self, step)
        self.updateLocations()
        self.locationsUpdated.emit()
        
    @Slot(str)
    def loginWithCode(self, code):
        self.setAuthAccess(code)
        self.login()
    
    @Slot()
    def stop(self):
        Crawler.stop(self)
    
    @Slot()  
    def createNewSearch(self):
        self.db.deleteLastSearch()
        self.createSearch()
        
    @Slot(float, float, float, float)
    def startMapSearch(self, lat1, long1, lat2, long2):
        self.addSearchStep()
        self.changed.emit()
        self.trackTweetsInsideArea(lat1, long1, lat2, long2)
    
    def updateLocations(self):
        loc = self.db.getStepInfo(self.step, self.last_id)
        self._locations = []
        for l in loc:
            if l[0] > self.last_id:
                self.last_id = l[0] 
            tmp = {}
            tmp["id"] = l[0]
            tmp["username"] = l[1]
            tmp["date"] = l[2]
            tmp["lat"] = l[3]
            tmp["lon"] = l[4]
            self._locations.append(tmp)
    
    def getLocations(self):
        return self._locations
    
    @Slot("QVariant")
    def getPointInfo(self, points):
        self._pointsInfo = {"users":[], "hashtags": [], "links": []}
        for p in points:
            info = self.db.getUser(p)
            self._pointsInfo["users"].append([info[0], info[2]])
        hashtags = self.db.getHashTagsOf(points)
        for h in hashtags:
            self._pointsInfo["hashtags"].append([h[0], h[1]])
        links = self.db.getLinksOf(points)
        for l in links:
            self._pointsInfo["links"].append([l[0], l[1]])
        self.pointInfoPrepared.emit()
        
        
        
    def getPiResult(self):
        return self._pointsInfo
    
    changed = Signal()
    loginChanged = Signal()
    locationsUpdated = Signal()
    pointInfoPrepared = Signal()
    loginUrl = Property(unicode, getAuthUrl, notify=loginChanged)
    loggedIn = Property(bool, login, notify=changed)
    _search = Property(str, getSearch, notify=changed)
    step = Property(str, getSteps, notify=changed)
    locations = Property("QVariant", getLocations, notify=locationsUpdated)
    pointsInfo = Property("QVariant", getPiResult, notify=pointInfoPrepared)

if __name__ == "__main__":
    frontend = os.path.join(os.path.realpath(os.path.dirname(__file__)), "frontend")
    app = QApplication(sys.argv)
    qmlRegisterType(Controller, "TwitterCrawler", 1, 0, "Controller")
    
    view = QDeclarativeView()
    glw = QGLWidget()
    view.setViewport(glw)
    view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
    root = view.rootContext()

    view.setSource(os.path.join(frontend, "frontend.qml"))
    view.show()
    
    app.exec_()
    sys.exit()               