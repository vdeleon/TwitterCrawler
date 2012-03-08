'''
Created on 07/mar/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''

from PySide.QtCore import *
from PySide.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.showFullScreen()