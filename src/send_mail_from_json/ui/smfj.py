# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'smfj.ui'
#
# Created by: Qt User Interface Compiler version 6.8.0
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QLabel, QPushButton,
                               QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(271, 172)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(70, 10, 131, 31))
        font = QFont()
        font.setFamilies([u"STZhongsong"])
        font.setPointSize(16)
        self.title.setFont(font)
        self.chooseProfileButton = QPushButton(self.centralwidget)
        self.chooseProfileButton.setObjectName(u"chooseProfileButton")
        self.chooseProfileButton.setGeometry(QRect(10, 50, 251, 51))
        self.sendMailButton = QPushButton(self.centralwidget)
        self.sendMailButton.setObjectName(u"sendMailButton")
        self.sendMailButton.setGeometry(QRect(10, 110, 251, 51))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u53d1\u9001\u90ae\u4ef6",
                                                             None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u53d1\u9001\u90ae\u4ef6", None))
        self.chooseProfileButton.setText(QCoreApplication.translate(
            "MainWindow",
            u"\u70b9\u51fb\u9009\u62e9JSON\u914d\u7f6e\u6587\u4ef6",
            None))
        self.sendMailButton.setText(QCoreApplication.translate(
            "MainWindow",
            u"\u70b9\u51fb\u4f9d\u7167\u914d\u7f6e\u6587\u4ef6\u81ea\u52a8\u53d1\u9001\u90ae\u4ef6",
            None))
    # retranslateUi
