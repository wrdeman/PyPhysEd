#!/usr/bin/python
"""
Module for opencv tracking of objects

"""
__author__ = 'wrdeman'
__version__ = '0/0'

import sys
import cv2
from PyQt4 import QtGui, QtCore, Qt
from ui import Ui_MainWindow
from Video import Video

class Gui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.video = Video(cv2.VideoCapture(0))
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
        self.update()
 
    def play(self):
        '''
        capture frame and display
        '''
        try:
            self.video.capture_next_frame()
            self.ui.videoFrame.setPixmap(
                self.video.convert_frame())
            self.ui.videoFrame.setScaledContents(True)
        except TypeError:
            print "No frame"


    def mousePressEvent(self, event):
        '''
        click mouse and put point on opencv window
        '''
        self.video.add_point(QtCore.QPoint(event.pos()), 
                            self.ui.videoFrame.geometry())

   
def main():
    '''
    main PyQt GUI
    '''
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

