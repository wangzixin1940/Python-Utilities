# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'pc.ui'
#
# Created by: Qt User Interface Compiler version 6.8.0
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QCheckBox, QGroupBox, QLabel,
                               QLineEdit, QPushButton, QSpinBox, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(279, 316)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(90, 20, 111, 31))
        font = QFont()
        font.setFamilies([u"STZhongsong"])
        font.setPointSize(16)
        self.title.setFont(font)
        self.digitsInputLabel = QLabel(self.centralwidget)
        self.digitsInputLabel.setObjectName(u"digitsInputLabel")
        self.digitsInputLabel.setGeometry(QRect(50, 70, 61, 21))
        font1 = QFont()
        font1.setFamilies([u"STZhongsong"])
        font1.setPointSize(10)
        self.digitsInputLabel.setFont(font1)
        self.digitsInput = QSpinBox(self.centralwidget)
        self.digitsInput.setObjectName(u"digitsInput")
        self.digitsInput.setGeometry(QRect(110, 70, 111, 22))
        self.optionsBox = QGroupBox(self.centralwidget)
        self.optionsBox.setObjectName(u"optionsBox")
        self.optionsBox.setGeometry(QRect(90, 100, 111, 111))
        self.includeUppers = QCheckBox(self.optionsBox)
        self.includeUppers.setObjectName(u"includeUppers")
        self.includeUppers.setGeometry(QRect(10, 40, 91, 21))
        self.includeSymbols = QCheckBox(self.optionsBox)
        self.includeSymbols.setObjectName(u"includeSymbols")
        self.includeSymbols.setGeometry(QRect(10, 60, 78, 20))
        self.includeNumbers = QCheckBox(self.optionsBox)
        self.includeNumbers.setObjectName(u"includeNumbers")
        self.includeNumbers.setGeometry(QRect(10, 80, 78, 20))
        self.includeLowers = QCheckBox(self.optionsBox)
        self.includeLowers.setObjectName(u"includeLowers")
        self.includeLowers.setEnabled(False)
        self.includeLowers.setGeometry(QRect(10, 20, 91, 20))
        self.includeLowers.setCheckable(True)
        self.includeLowers.setChecked(True)
        self.includeLowers.setTristate(False)
        self.generateButton = QPushButton(self.centralwidget)
        self.generateButton.setObjectName(u"generateButton")
        self.generateButton.setGeometry(QRect(50, 220, 75, 24))
        self.copyButton = QPushButton(self.centralwidget)
        self.copyButton.setObjectName(u"copyButton")
        self.copyButton.setGeometry(QRect(150, 220, 75, 24))
        self.passwordDisplay = QLineEdit(self.centralwidget)
        self.passwordDisplay.setObjectName(u"passwordDisplay")
        self.passwordDisplay.setEnabled(False)
        self.passwordDisplay.setGeometry(QRect(50, 260, 181, 21))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801\u751f\u6210\u5668", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801\u751f\u6210\u5668", None))
        self.digitsInputLabel.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801\u4f4d\u6570\uff1a", None))
        self.optionsBox.setTitle(QCoreApplication.translate("MainWindow", u"\u9009\u9879", None))
        self.includeUppers.setText(QCoreApplication.translate("MainWindow", u"\u63d2\u5165\u5927\u5199\u5b57\u6bcd",
                                                              None))
        self.includeSymbols.setText(QCoreApplication.translate("MainWindow", u"\u63d2\u5165\u7b26\u53f7", None))
        self.includeNumbers.setText(QCoreApplication.translate("MainWindow", u"\u63d2\u5165\u6570\u5b57", None))
        self.includeLowers.setText(QCoreApplication.translate("MainWindow", u"\u63d2\u5165\u5c0f\u5199\u5b57\u6bcd",
                                                              None))
        self.generateButton.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210", None))
        self.copyButton.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236", None))
    # retranslateUi
