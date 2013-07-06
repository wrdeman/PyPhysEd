#!/opt/local/bin/python
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
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.video = Video(cv2.VideoCapture(0))
        self._timer = QtCore.QTimer(self)
        self.run = False
        self.plot = False
        self._timer.timeout.connect(self.changeStartStop)
        self._timer.start(10)
        self.update()
        #connect the start / stop button
        QtCore.QObject.connect(self.ui.startVideoButton,
                               QtCore.SIGNAL("clicked()"),
                               self.changeStartStop)

        # connect the file open button
        QtCore.QObject.connect(self.ui.actionOpen,
                               QtCore.SIGNAL("triggered()"),
                               self.openFile)

        # connect the close button
        QtCore.QObject.connect(self.ui.actionQuit,
                               QtCore.SIGNAL("triggered()"),
                               self.close)

        # connect the close button
        QtCore.QObject.connect(self.ui.actionGraph,
                               QtCore.SIGNAL("triggered()"),
                               self.plotOn)

    def changeStartStop(self):
        if self.run:
            self.run = False
            self.ui.startVideoButton.setText('Start')
            self.capture()
        else:
            self.run = True
            self.ui.startVideoButton.setText('Stop')

#        def selectInput(self):
#        '''
#         default camera
#        select file or camera
#        must lead to separate file
#        '''

    def capture(self):
        """
        gets the video frame and converts it Qt format
        """
        try:
            self.video.captureNextFrame(self.plot)
            self.ui.videoFrame.setPixmap(
                self.video.convertFrame())
            self.ui.videoFrame.setScaledContents(True)
        except TypeError:
            self.stop()

    def openFile(self):
        openfile=QtGui.QFileDialog()
        openfile.setOption(QtGui.QFileDialog.DontUseNativeDialog)
        fname=openfile.getOpenFileName(self,'Open file','.')
        if isfile(fname):
            self.capture = cv2.VideoCapture(str(fname))                

    def acionQuit(self):
        self.close()

    def plotOn(self):
        if self.plot:
            self.plot=False
        else:
            self.plot=True

    def mousePressEvent(self, event):
        self.video.addPoint(QtCore.QPoint(event.pos()),
                            self.ui.videoFrame.geometry())

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
#        if e.key() == QtCore.Qt.Key_Backspace:
#            self.features.pop(len(self.features)-1)

   
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

