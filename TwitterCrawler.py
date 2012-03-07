'''
Created on 15/feb/2012

@author: Riccardo Ferrazzo <f.riccardo87@gmail.com>
'''
import sys
from PySide.QtCore import *
from frontend.MainWindow import *

app = QApplication(sys.argv)
win = MainWindow()
win.show()

app.exec_()
sys.exit()        