'''
Created on 15/feb/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import sys, os.path
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *

app = QApplication(sys.argv)

view = QDeclarativeView()
context = view.rootContext()
view.setSource(os.path.join(os.path.realpath(os.path.dirname(__file__)), "frontend", "frontend.qml"))
view.show()

app.exec_()
sys.exit()        