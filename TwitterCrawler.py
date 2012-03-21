'''
Created on 15/feb/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import sys, os.path
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from PySide.QtOpenGL import *

from backend.SearchManager import SearchManager

class Controller(QObject):
    sm = SearchManager()
    changed = Signal()
    loginChanged = Signal()

    def login(self):
        return self.sm.crawler.login()
    
    def _loginUrl(self):
        return self.sm.crawler.getAuthUrl()
    
    def _search(self):
        if self.sm.search != None:
            return "Temp"
        return "None"
    
    def _step(self):
        return str(self.sm.step)
    
    @Slot(str)
    def loginWithCode(self, code):
        self.sm.crawler.setAuthAccess(code)
        self.sm.crawler.login()
    
    @Slot()  
    def createNewSearch(self):
        self.sm.createSearch()
        self.changed.emit()
        
    @Slot(float, float, float, float)
    def startMapSearch(self, lat1, long1, lat2, long2):
        self.sm.addSearchStep()
        self.changed.emit()
        self.sm.crawler.trackTweetsInsideArea(lat1, long1, lat2, long2)
    
    loginUrl = Property(unicode, _loginUrl, notify=loginChanged)
    loggedIn = Property(bool, login, notify=changed)
    search = Property(str, _search, notify=changed)
    step = Property(str, _step, notify=changed)

if __name__ == "__main__":
    frontend = os.path.join(os.path.realpath(os.path.dirname(__file__)), "frontend")
    app = QApplication(sys.argv)
    
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