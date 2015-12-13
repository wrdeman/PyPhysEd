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
from snapUI import Ui_Form
from Video import Video
import time

class Popup(QtGui.QMainWindow):
    '''Pop up window to define tracking parameters'''
    def __init__(self,calibParams):
        self.calibParams=calibParams
        self.snap = Ui_Form()
        self.snap.setupUi(self)

        QtGui.QWidget.__init__(self)

        QtCore.QObject.connect(self.snap.tableData,
                               QtCore.SIGNAL("cellChanged(int, int)"),
                               self.getParams)
        QtCore.QObject.connect(self.snap.snapShot,
                               QtCore.SIGNAL("clicked()"),
                               self.close)

    def getParams(self):
        for i in range(len(self.calibParams)):
            if i<2:
                self.calibParams[i]=int(self.snap.tableData.item(i, 0).text())
            else:
                self.calibParams[i]=float(self.snap.tableData.item(i, 0).text())


class Gui(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.video = Video(cv2.VideoCapture(0))
        self._timer = QtCore.QTimer(self)
        self.run = False
        self.plot = False
        self.ui.comboYAxis.setCurrentIndex(1)
        self._timer.timeout.connect(self.capture)
        self._timer.start(10)
        self.update()
        self.dt = 0
        self.calibParams=[1,1]
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

        # connect the graph button
        QtCore.QObject.connect(self.ui.actionGraph,
                               QtCore.SIGNAL("triggered()"),
                               self.plotOn)

        # connect the calib button
        QtCore.QObject.connect(self.ui.actionCalib,
                               QtCore.SIGNAL("triggered()"),
                               self.calibDialog)

        QtCore.QObject.connect(self.ui.comboXAxis,
                               QtCore.SIGNAL("currentIndexChanged(QString)"),self.changeXAxis)

        QtCore.QObject.connect(self.ui.comboYAxis,
                               QtCore.SIGNAL("currentIndexChanged(QString)"),self.changeYAxis)
                               


    def calibDialog(self):
        self.pop=Popup(self.calibParams)
        self.pop.show()

    def changeXAxis(self):
        self.video.changeXAxis(
            int(self.ui.comboXAxis.currentIndex())
        )

    def changeYAxis(self):
        self.video.changeYAxis(
            int(self.ui.comboYAxis.currentIndex())
        )

    def changeStartStop(self):
        if self.run:
            self.run = False
            self.ui.startVideoButton.setText('Start')
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
        start = time.time()
        if self.run:
            try:
                self.video.captureNextFrame(self.plot,self.dt)
                self.ui.videoFrame.setPixmap(
                    self.video.convertFrame())
                self.ui.videoFrame.setScaledContents(True)
            except TypeError:
                self.run = False
        self.dt = int(1000*(time.time()-start))

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
        if (event.button() == QtCore.Qt.LeftButton
            and QtGui.QApplication.keyboardModifiers()
            ==QtCore.Qt.ShiftModifier):
            self.video.addOrigin(QtCore.QPoint(event.pos()),
                                self.ui.videoFrame.geometry())
        
        else:
            self.video.addPoint(QtCore.QPoint(event.pos()),
                                self.ui.videoFrame.geometry())


    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        if e.key() == QtCore.Qt.Key_Return:
            #return becasue mac os x
            self.video.deleteLastPoint()

   
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

