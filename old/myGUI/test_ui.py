# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myGUI/mainwindow.ui'
#
# Created: Wed Apr 25 19:59:17 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(600, 600)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.video_lbl = QtGui.QLabel(self.centralWidget)
        self.video_lbl.setGeometry(QtCore.QRect(20, 20, 200, 200))
        self.video_lbl.setText(_fromUtf8(""))
        self.video_lbl.setObjectName(_fromUtf8("video_lbl"))
        self.video_plt = Qwt5.QwtPlot(self.centralWidget)
        self.video_plt.setGeometry(QtCore.QRect(240, 20, 200, 200))
        self.video_plt.setObjectName(_fromUtf8("video_plt"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 600, 20))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuInput = QtGui.QMenu(self.menuFile)
        self.menuInput.setTitle(QtGui.QApplication.translate("MainWindow", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.menuInput.setObjectName(_fromUtf8("menuInput"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionFile = QtGui.QAction(MainWindow)
        self.actionFile.setText(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFile.setObjectName(_fromUtf8("actionFile"))
        self.actionCam = QtGui.QAction(MainWindow)
        self.actionCam.setText(QtGui.QApplication.translate("MainWindow", "Cam", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCam.setObjectName(_fromUtf8("actionCam"))
        self.menuInput.addAction(self.actionFile)
        self.menuInput.addAction(self.actionCam)
        self.menuFile.addAction(self.menuInput.menuAction())
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

from PyQt4 import Qwt5
