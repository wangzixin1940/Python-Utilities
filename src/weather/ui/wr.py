# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'wr.ui'
#
# Created by: Qt User Interface Compiler version 6.8.0
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QGroupBox, QLabel, QLineEdit,
                               QListWidget, QListWidgetItem, QPushButton,
                               QScrollArea, QSpinBox, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(341, 421)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(110, 20, 131, 21))
        font = QFont()
        font.setFamilies([u"FZYaoTi"])
        font.setPointSize(16)
        self.title.setFont(font)
        self.queryBox = QGroupBox(self.centralwidget)
        self.queryBox.setObjectName(u"queryBox")
        self.queryBox.setGeometry(QRect(10, 40, 321, 151))
        self.areaCodeEdit = QSpinBox(self.queryBox)
        self.areaCodeEdit.setObjectName(u"areaCodeEdit")
        self.areaCodeEdit.setGeometry(QRect(10, 110, 301, 22))
        self.areaCodeEdit.setMaximum(9999)
        self.countryEdit = QLineEdit(self.queryBox)
        self.countryEdit.setObjectName(u"countryEdit")
        self.countryEdit.setGeometry(QRect(50, 20, 261, 21))
        self.cityEdit = QLineEdit(self.queryBox)
        self.cityEdit.setObjectName(u"cityEdit")
        self.cityEdit.setGeometry(QRect(50, 50, 261, 21))
        self.countyEdit = QLineEdit(self.queryBox)
        self.countyEdit.setObjectName(u"countyEdit")
        self.countyEdit.setGeometry(QRect(50, 80, 261, 21))
        self.countryLabel = QLabel(self.queryBox)
        self.countryLabel.setObjectName(u"countryLabel")
        self.countryLabel.setGeometry(QRect(0, 20, 53, 16))
        self.countryLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                       Qt.AlignmentFlag.AlignVCenter)
        self.cityLabel = QLabel(self.queryBox)
        self.cityLabel.setObjectName(u"cityLabel")
        self.cityLabel.setGeometry(QRect(0, 50, 53, 16))
        self.cityLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                    Qt.AlignmentFlag.AlignVCenter)
        self.countyLabel = QLabel(self.queryBox)
        self.countyLabel.setObjectName(u"countyLabel")
        self.countyLabel.setGeometry(QRect(0, 80, 53, 16))
        self.countyLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                      Qt.AlignmentFlag.AlignVCenter)
        self.favouritesBox = QGroupBox(self.centralwidget)
        self.favouritesBox.setObjectName(u"favouritesBox")
        self.favouritesBox.setGeometry(QRect(10, 190, 321, 181))
        self.scrollArea = QScrollArea(self.favouritesBox)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(0, 20, 321, 161))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 500, 1000))
        self.scrollAreaWidgetContents.setMinimumSize(QSize(500, 1000))
        self.favouritesDisplay = QListWidget(self.scrollAreaWidgetContents)
        QListWidgetItem(self.favouritesDisplay)
        QListWidgetItem(self.favouritesDisplay)
        QListWidgetItem(self.favouritesDisplay)
        QListWidgetItem(self.favouritesDisplay)
        self.favouritesDisplay.setObjectName(u"favouritesDisplay")
        self.favouritesDisplay.setGeometry(QRect(0, 0, 501, 1001))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.queryButton = QPushButton(self.centralwidget)
        self.queryButton.setObjectName(u"queryButton")
        self.queryButton.setGeometry(QRect(10, 380, 321, 31))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u5929\u6c14\u9884\u62a5", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u5929\u6c14\u9884\u62a5\u7a0b\u5e8f", None))
        self.queryBox.setTitle(QCoreApplication.translate("MainWindow", u"\u5b9e\u65f6\u67e5\u8be2", None))
        self.countryLabel.setText(QCoreApplication.translate("MainWindow", u"\u56fd\u5bb6\uff1a", None))
        self.cityLabel.setText(QCoreApplication.translate("MainWindow", u"\u57ce\u5e02\uff1a", None))
        self.countyLabel.setText(QCoreApplication.translate("MainWindow", u"\u90e1\u53bf\uff1a", None))
        self.favouritesBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6536\u85cf\u5730\u533a", None))

        __sortingEnabled = self.favouritesDisplay.isSortingEnabled()
        self.favouritesDisplay.setSortingEnabled(False)
        ___qlistwidgetitem = self.favouritesDisplay.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"China, Beijing, 237", None))
        ___qlistwidgetitem1 = self.favouritesDisplay.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow",
                                                               u"United States of America, Washington DC, 270", None))
        ___qlistwidgetitem2 = self.favouritesDisplay.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow",
                                                               u"United Kingdom of Great Britain and Northern Ireland, "
                                                               u"London, 32", None))
        ___qlistwidgetitem3 = self.favouritesDisplay.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"France, Paris, 194", None))
        self.favouritesDisplay.setSortingEnabled(__sortingEnabled)

        self.queryButton.setText(QCoreApplication.translate("MainWindow", u"\u73b0\u5728\u67e5\u8be2", None))
    # retranslateUi
