# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/snapImage.ui'
#
# Created: Tue Jul  9 23:38:29 2013
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(352, 219)
        self.tableData = QtGui.QTableWidget(Form)
        self.tableData.setGeometry(QtCore.QRect(50, 30, 241, 51))
        self.tableData.setObjectName(_fromUtf8("tableData"))
        self.tableData.setColumnCount(2)
        self.tableData.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.tableData.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableData.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableData.setHorizontalHeaderItem(1, item)
        self.snapShot = QtGui.QPushButton(Form)
        self.snapShot.setGeometry(QtCore.QRect(50, 100, 251, 71))
        self.snapShot.setObjectName(_fromUtf8("snapShot"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        item = self.tableData.verticalHeaderItem(0)
        item.setText(_translate("Form", "Input", None))
        item = self.tableData.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Checkersize (cm)", None))
        item = self.tableData.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Length (cm)", None))
        self.snapShot.setText(_translate("Form", "SnapShot", None))

