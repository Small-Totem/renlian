# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(600, 450))
        MainWindow.setMaximumSize(QtCore.QSize(600, 450))
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.commandLinkButton_start_write_diary = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton_start_write_diary.setGeometry(QtCore.QRect(410, 380, 171, 48))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.commandLinkButton_start_write_diary.setFont(font)
        self.commandLinkButton_start_write_diary.setObjectName("commandLinkButton_start_write_diary")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 100, 561, 71))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.commandLinkButton_settings = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton_settings.setGeometry(QtCore.QRect(20, 380, 181, 48))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.commandLinkButton_settings.setFont(font)
        self.commandLinkButton_settings.setObjectName("commandLinkButton_settings")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 561, 71))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "隐私日记本"))
        self.commandLinkButton_start_write_diary.setText(_translate("MainWindow", "开始写日记!"))
        self.label.setText(_translate("MainWindow", "隐私日记本是一款保护隐私的日记软件, 用户可以录入人脸并通过人脸识别打开自己的日记!"))
        self.commandLinkButton_settings.setText(_translate("MainWindow", "开始录入人脸"))
        self.label_2.setText(_translate("MainWindow", "欢迎!"))
