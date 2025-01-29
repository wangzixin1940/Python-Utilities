# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'st.ui'
#
# Created by: Qt User Interface Compiler version 6.8.0
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QLCDNumber, QLabel, QPushButton, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(297, 205)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(100, 10, 91, 31))
        font = QFont()
        font.setFamilies([u"STZhongsong"])
        font.setPointSize(16)
        self.title.setFont(font)
        self.uploadLabel = QLabel(self.centralwidget)
        self.uploadLabel.setObjectName(u"uploadLabel")
        self.uploadLabel.setGeometry(QRect(70, 60, 61, 21))
        self.uploadSpeed = QLCDNumber(self.centralwidget)
        self.uploadSpeed.setObjectName(u"uploadSpeed")
        self.uploadSpeed.setGeometry(QRect(130, 60, 64, 23))
        self.mbpsSign = QLabel(self.centralwidget)
        self.mbpsSign.setObjectName(u"mbpsSign")
        self.mbpsSign.setGeometry(QRect(200, 60, 53, 21))
        self.downloadLabel = QLabel(self.centralwidget)
        self.downloadLabel.setObjectName(u"downloadLabel")
        self.downloadLabel.setGeometry(QRect(70, 90, 61, 21))
        self.downloadSpeed = QLCDNumber(self.centralwidget)
        self.downloadSpeed.setObjectName(u"downloadSpeed")
        self.downloadSpeed.setGeometry(QRect(130, 90, 64, 23))
        self.mbpsSign_2 = QLabel(self.centralwidget)
        self.mbpsSign_2.setObjectName(u"mbpsSign_2")
        self.mbpsSign_2.setGeometry(QRect(200, 90, 53, 21))
        self.testButton = QPushButton(self.centralwidget)
        self.testButton.setObjectName(u"testButton")
        self.testButton.setGeometry(QRect(70, 120, 161, 31))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u7f51\u901f\u6d4b\u8bd5", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u901f\u6d4b\u8bd5", None))
        self.uploadLabel.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4f20\u7f51\u901f\uff1a", None))
        self.mbpsSign.setText(QCoreApplication.translate("MainWindow", u"Mb/S", None))
        self.downloadLabel.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d\u7f51\u901f\uff1a", None))
        self.mbpsSign_2.setText(QCoreApplication.translate("MainWindow", u"Mb/S", None))
        self.testButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u6d4b\u91cf", None))
    # retranslateUi

