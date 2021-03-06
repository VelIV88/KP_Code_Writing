# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\iapen\Projects\python\KP\TMM\ui\WindowCrancRod.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widgetResult = QtWidgets.QWidget(self.centralwidget)
        self.widgetResult.setGeometry(QtCore.QRect(10, 60, 480, 500))
        self.widgetResult.setObjectName("widgetResult")
        self.labelTitleGraph = QtWidgets.QLabel(self.centralwidget)
        self.labelTitleGraph.setGeometry(QtCore.QRect(10, 10, 200, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.labelTitleGraph.setFont(font)
        self.labelTitleGraph.setObjectName("labelTitleGraph")
        self.toolButtonPosition = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonPosition.setGeometry(QtCore.QRect(520, 460, 250, 30))
        self.toolButtonPosition.setObjectName("toolButtonPosition")
        self.toolButtonSpeed = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonSpeed.setGeometry(QtCore.QRect(520, 500, 250, 30))
        self.toolButtonSpeed.setObjectName("toolButtonSpeed")
        self.toolButtonAcceliration = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonAcceliration.setGeometry(QtCore.QRect(520, 540, 250, 30))
        self.toolButtonAcceliration.setObjectName("toolButtonAcceliration")
        self.labelAngleGuid = QtWidgets.QLabel(self.centralwidget)
        self.labelAngleGuid.setGeometry(QtCore.QRect(520, 210, 45, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.labelAngleGuid.setFont(font)
        self.labelAngleGuid.setObjectName("labelAngleGuid")
        self.textInAngleGuid = QtWidgets.QTextEdit(self.centralwidget)
        self.textInAngleGuid.setGeometry(QtCore.QRect(580, 210, 190, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textInAngleGuid.setFont(font)
        self.textInAngleGuid.setObjectName("textInAngleGuid")
        self.textInEccentrGuid = QtWidgets.QTextEdit(self.centralwidget)
        self.textInEccentrGuid.setGeometry(QtCore.QRect(580, 250, 190, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textInEccentrGuid.setFont(font)
        self.textInEccentrGuid.setObjectName("textInEccentrGuid")
        self.labelEccentrGuid = QtWidgets.QLabel(self.centralwidget)
        self.labelEccentrGuid.setGeometry(QtCore.QRect(520, 250, 45, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.labelEccentrGuid.setFont(font)
        self.labelEccentrGuid.setObjectName("labelEccentrGuid")
        self.labelRotateSpeed = QtWidgets.QLabel(self.centralwidget)
        self.labelRotateSpeed.setGeometry(QtCore.QRect(520, 290, 45, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.labelRotateSpeed.setFont(font)
        self.labelRotateSpeed.setObjectName("labelRotateSpeed")
        self.textInRotateSpeed = QtWidgets.QTextEdit(self.centralwidget)
        self.textInRotateSpeed.setGeometry(QtCore.QRect(580, 290, 190, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textInRotateSpeed.setFont(font)
        self.textInRotateSpeed.setObjectName("textInRotateSpeed")
        self.textInAngleCrank = QtWidgets.QTextEdit(self.centralwidget)
        self.textInAngleCrank.setGeometry(QtCore.QRect(580, 410, 190, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textInAngleCrank.setFont(font)
        self.textInAngleCrank.setObjectName("textInAngleCrank")
        self.textInLengthCrank = QtWidgets.QTextEdit(self.centralwidget)
        self.textInLengthCrank.setGeometry(QtCore.QRect(580, 330, 190, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textInLengthCrank.setFont(font)
        self.textInLengthCrank.setObjectName("textInLengthCrank")
        self.labelAngleCrank = QtWidgets.QLabel(self.centralwidget)
        self.labelAngleCrank.setGeometry(QtCore.QRect(520, 410, 45, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.labelAngleCrank.setFont(font)
        self.labelAngleCrank.setObjectName("labelAngleCrank")
        self.labelLengthRod = QtWidgets.QLabel(self.centralwidget)
        self.labelLengthRod.setGeometry(QtCore.QRect(520, 370, 45, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.labelLengthRod.setFont(font)
        self.labelLengthRod.setObjectName("labelLengthRod")
        self.textInLengthRod = QtWidgets.QTextEdit(self.centralwidget)
        self.textInLengthRod.setGeometry(QtCore.QRect(580, 370, 190, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textInLengthRod.setFont(font)
        self.textInLengthRod.setObjectName("textInLengthRod")
        self.labelLengthCrank = QtWidgets.QLabel(self.centralwidget)
        self.labelLengthCrank.setGeometry(QtCore.QRect(520, 330, 45, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.labelLengthCrank.setFont(font)
        self.labelLengthCrank.setObjectName("labelLengthCrank")
        self.labelLog = QtWidgets.QLabel(self.centralwidget)
        self.labelLog.setGeometry(QtCore.QRect(520, 60, 250, 135))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelLog.setFont(font)
        self.labelLog.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelLog.setObjectName("labelLog")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelTitleGraph.setText(_translate("MainWindow", "???????????????????????? ????????????"))
        self.toolButtonPosition.setText(_translate("MainWindow", "?????????????????? ?????????????????? ??????????????????"))
        self.toolButtonSpeed.setText(_translate("MainWindow", "?????????????????? ???????? ??????????????????"))
        self.toolButtonAcceliration.setText(_translate("MainWindow", "?????????????????? ???????? ??????????????????"))
        self.labelAngleGuid.setText(_translate("MainWindow", "?? ="))
        self.labelEccentrGuid.setText(_translate("MainWindow", "e ="))
        self.labelRotateSpeed.setText(_translate("MainWindow", "?? ="))
        self.labelAngleCrank.setText(_translate("MainWindow", "?? ="))
        self.labelLengthRod.setText(_translate("MainWindow", "lBA ="))
        self.labelLengthCrank.setText(_translate("MainWindow", "lOA ="))
