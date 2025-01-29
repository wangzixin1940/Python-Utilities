# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'pfc.ui'
#
# Created by: Qt User Interface Compiler version 6.8.0
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QComboBox, QLabel, QPushButton, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(244, 192)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(50, 10, 151, 31))
        font = QFont()
        font.setFamilies([u"STZhongsong"])
        font.setPointSize(16)
        self.title.setFont(font)
        self.choosePhotoButton = QPushButton(self.centralwidget)
        self.choosePhotoButton.setObjectName(u"choosePhotoButton")
        self.choosePhotoButton.setGeometry(QRect(40, 50, 161, 31))
        self.convertOptions = QComboBox(self.centralwidget)
        self.convertOptions.addItem("")
        self.convertOptions.addItem("")
        self.convertOptions.addItem("")
        self.convertOptions.addItem("")
        self.convertOptions.setObjectName(u"convertOptions")
        self.convertOptions.setGeometry(QRect(110, 90, 91, 31))
        self.convertOptionsLabel = QLabel(self.centralwidget)
        self.convertOptionsLabel.setObjectName(u"convertOptionsLabel")
        self.convertOptionsLabel.setGeometry(QRect(40, 95, 61, 21))
        font1 = QFont()
        font1.setPointSize(11)
        self.convertOptionsLabel.setFont(font1)
        self.convertButton = QPushButton(self.centralwidget)
        self.convertButton.setObjectName(u"convertButton")
        self.convertButton.setGeometry(QRect(40, 130, 161, 31))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u7167\u7247\u683c\u5f0f"
                                                                           u"\u8f6c\u6362\u5668", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u7167\u7247\u683c\u5f0f\u8f6c\u6362\u5668",
                                                      None))
        self.choosePhotoButton.setText(QCoreApplication.translate("MainWindow", u"\u70b9\u51fb\u9009\u62e9\u7167\u7247",
                                                                  None))
        self.convertOptions.setItemText(0, QCoreApplication.translate("MainWindow", u"JPG", None))
        self.convertOptions.setItemText(1, QCoreApplication.translate("MainWindow", u"PNG", None))
        self.convertOptions.setItemText(2, QCoreApplication.translate("MainWindow", u"GIF", None))
        self.convertOptions.setItemText(3, QCoreApplication.translate("MainWindow", u"BMP", None))

        self.convertOptionsLabel.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u6362\u4e3a\uff1a", None))
        self.convertButton.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u6362\u5e76\u4fdd\u5b58", None))
    # retranslateUi
