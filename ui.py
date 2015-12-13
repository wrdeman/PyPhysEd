# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/mainWindow.ui'
#
# Created: Tue Jul  9 22:58:13 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(801, 649)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.videoFrame = QtGui.QLabel(self.centralwidget)
        self.videoFrame.setGeometry(QtCore.QRect(120, -10, 611, 501))
        self.videoFrame.setAutoFillBackground(True)
        self.videoFrame.setText(_fromUtf8(""))
        self.videoFrame.setObjectName(_fromUtf8("videoFrame"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(110, 550, 389, 32))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.startVideoButton = QtGui.QPushButton(self.layoutWidget)
        self.startVideoButton.setObjectName(_fromUtf8("startVideoButton"))
        self.horizontalLayout.addWidget(self.startVideoButton)
        self.comboXAxis = QtGui.QComboBox(self.layoutWidget)
        self.comboXAxis.setObjectName(_fromUtf8("comboXAxis"))
        self.comboXAxis.addItem(_fromUtf8(""))
        self.comboXAxis.addItem(_fromUtf8(""))
        self.comboXAxis.addItem(_fromUtf8(""))
        self.comboXAxis.addItem(_fromUtf8(""))
        self.comboXAxis.addItem(_fromUtf8(""))
        self.comboXAxis.addItem(_fromUtf8(""))
        self.comboXAxis.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboXAxis)
        self.comboYAxis = QtGui.QComboBox(self.layoutWidget)
        self.comboYAxis.setObjectName(_fromUtf8("comboYAxis"))
        self.comboYAxis.addItem(_fromUtf8(""))
        self.comboYAxis.addItem(_fromUtf8(""))
        self.comboYAxis.addItem(_fromUtf8(""))
        self.comboYAxis.addItem(_fromUtf8(""))
        self.comboYAxis.addItem(_fromUtf8(""))
        self.comboYAxis.addItem(_fromUtf8(""))
        self.comboYAxis.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboYAxis)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuPlot = QtGui.QMenu(self.menubar)
        self.menuPlot.setObjectName(_fromUtf8("menuPlot"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionGraph = QtGui.QAction(MainWindow)
        self.actionGraph.setObjectName(_fromUtf8("actionGraph"))
        self.actionCalib = QtGui.QAction(MainWindow)
        self.actionCalib.setObjectName(_fromUtf8("actionCalib"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionQuit)
        self.menuPlot.addAction(self.actionGraph)
        self.menuPlot.addAction(self.actionCalib)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPlot.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.startVideoButton.setText(_translate("MainWindow", "Start", None))
        self.comboXAxis.setItemText(0, _translate("MainWindow", "t", None))
        self.comboXAxis.setItemText(1, _translate("MainWindow", "amplitude", None))
        self.comboXAxis.setItemText(2, _translate("MainWindow", "d(amplitude)/dt", None))
        self.comboXAxis.setItemText(3, _translate("MainWindow", "theta", None))
        self.comboXAxis.setItemText(4, _translate("MainWindow", "d(theta)/dt", None))
        self.comboXAxis.setItemText(5, _translate("MainWindow", "x", None))
        self.comboXAxis.setItemText(6, _translate("MainWindow", "y", None))
        self.comboYAxis.setItemText(0, _translate("MainWindow", "t", None))
        self.comboYAxis.setItemText(1, _translate("MainWindow", "amplitude", None))
        self.comboYAxis.setItemText(2, _translate("MainWindow", "d(amplitude)/dt", None))
        self.comboYAxis.setItemText(3, _translate("MainWindow", "theta", None))
        self.comboYAxis.setItemText(4, _translate("MainWindow", "d(theta)/dt", None))
        self.comboYAxis.setItemText(5, _translate("MainWindow", "x", None))
        self.comboYAxis.setItemText(6, _translate("MainWindow", "y", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuPlot.setTitle(_translate("MainWindow", "Plot", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionQuit.setToolTip(_translate("MainWindow", "Quit", None))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actionGraph.setText(_translate("MainWindow", "Graph", None))
        self.actionGraph.setShortcut(_translate("MainWindow", "G", None))
        self.actionCalib.setText(_translate("MainWindow", "Calib", None))

