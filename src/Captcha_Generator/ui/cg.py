# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'cg.ui'
#
# Created by: Qt User Interface Compiler version 6.8.0
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QGroupBox, QLabel, QPushButton, QRadioButton, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(204, 173)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(50, 10, 121, 31))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        font.setBold(True)
        self.title.setFont(font)
        self.choices = QGroupBox(self.centralwidget)
        self.choices.setObjectName(u"choices")
        self.choices.setGeometry(QRect(40, 40, 131, 80))
        self.pictureCaptchaChoice = QRadioButton(self.choices)
        self.pictureCaptchaChoice.setObjectName(u"pictureCaptchaChoice")
        self.pictureCaptchaChoice.setGeometry(QRect(20, 20, 93, 20))
        self.audioCaptchaChoice = QRadioButton(self.choices)
        self.audioCaptchaChoice.setObjectName(u"audioCaptchaChoice")
        self.audioCaptchaChoice.setGeometry(QRect(20, 50, 93, 20))
        self.generateButton = QPushButton(self.centralwidget)
        self.generateButton.setObjectName(u"generateButton")
        self.generateButton.setGeometry(QRect(40, 130, 131, 24))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u9a8c\u8bc1\u7801\u751f\u6210\u5668",
                                                             None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u9a8c\u8bc1\u7801\u751f\u6210\u5668", None))
        self.choices.setTitle(QCoreApplication.translate("MainWindow", u"\u9009\u9879", None))
        self.pictureCaptchaChoice.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u9a8c\u8bc1\u7801",
                                                                     None))
        self.audioCaptchaChoice.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u9891\u9a8c\u8bc1\u7801",
                                                                   None))
        self.generateButton.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210", None))
    # retranslateUi

