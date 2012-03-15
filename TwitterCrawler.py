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

    def login(self):
        return self.sm.crawler.login()
    
    def _loginUrl(self):
        return self.sm.crawler.getAuthUrl()
    
    @Signal
    def changed(self):
        pass
    
    loginUrl = Property(unicode, _loginUrl, notify=changed)
    loggedIn = Property(bool, login, notify=changed)

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