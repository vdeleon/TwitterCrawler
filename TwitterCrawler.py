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
        self.locationsUpdated.emit()
        
    @Slot(str)
    def loginWithCode(self, code):
        self.setAuthAccess(code)
        self.login()
    
    @Slot()  
    def createNewSearch(self):
        self.createSearch()
        self.changed.emit()
        
    @Slot(float, float, float, float)
    def startMapSearch(self, lat1, long1, lat2, long2):
        self.addSearchStep()
        self.changed.emit()
        self.trackTweetsInsideArea(lat1, long1, lat2, long2)
    
    def updateLocations(self):
        loc = self.db.getStepInfo(self.step)
        res = []
        for l in loc:
            tmp = {}
            tmp["id"] = l[0]
            tmp["username"] = l[1]
            tmp["date"] = l[2]
            tmp["lat"] = l[3]
            tmp["lon"] = l[4]
            res.append(tmp)
        return res
    
    changed = Signal()
    loginChanged = Signal()
    locationsUpdated = Signal()
    loginUrl = Property(unicode, getAuthUrl, notify=loginChanged)
    loggedIn = Property(bool, login, notify=changed)
    _search = Property(str, getSearch, notify=changed)
    step = Property(str, getSteps, notify=changed)
    locations = Property("QVariant", updateLocations, notify=locationsUpdated)

if __name__ == "__main__":
    frontend = os.path.join(os.path.realpath(os.path.dirname(__file__)), "frontend")
    app = QApplication(sys.argv)
    qmlRegisterType(Controller, "TwitterCrawler", 1, 0, "Controller")
    
    view = QDeclarativeView()
    glw = QGLWidget()
    view.setViewport(glw)
    view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
    root = view.rootContext()
    controller = Controller()
    
    root.setContextProperty('controller', controller)
    view.setSource(os.path.join(frontend, "frontend.qml"))
    view.show()
    
    app.exec_()
    sys.exit()               