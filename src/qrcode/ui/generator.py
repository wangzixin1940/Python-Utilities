# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'generator.ui'
#
# Created by: Qt User Interface Compiler version 6.8.0
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QComboBox, QGroupBox, QLabel,
                               QPlainTextEdit, QPushButton, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(347, 386)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(110, 10, 131, 31))
        font = QFont()
        font.setFamilies([u"STZhongsong"])
        font.setPointSize(16)
        self.title.setFont(font)
        self.inputBox = QGroupBox(self.centralwidget)
        self.inputBox.setObjectName(u"inputBox")
        self.inputBox.setGeometry(QRect(10, 40, 331, 171))
        self.textEdit = QPlainTextEdit(self.inputBox)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(10, 20, 311, 141))
        self.settingsBox = QGroupBox(self.centralwidget)
        self.settingsBox.setObjectName(u"settingsBox")
        self.settingsBox.setGeometry(QRect(10, 220, 331, 121))
        self.drawerChooseLabel = QLabel(self.settingsBox)
        self.drawerChooseLabel.setObjectName(u"drawerChooseLabel")
        self.drawerChooseLabel.setGeometry(QRect(20, 20, 81, 20))
        self.drawerChooseBox = QComboBox(self.settingsBox)
        self.drawerChooseBox.addItem("")
        self.drawerChooseBox.addItem("")
        self.drawerChooseBox.addItem("")
        self.drawerChooseBox.addItem("")
        self.drawerChooseBox.addItem("")
        self.drawerChooseBox.addItem("")
        self.drawerChooseBox.setObjectName(u"drawerChooseBox")
        self.drawerChooseBox.setGeometry(QRect(110, 20, 201, 22))
        self.colorMaskChooseLabel = QLabel(self.settingsBox)
        self.colorMaskChooseLabel.setObjectName(u"colorMaskChooseLabel")
        self.colorMaskChooseLabel.setGeometry(QRect(20, 50, 91, 20))
        self.colorMaskChooseBox = QComboBox(self.settingsBox)
        self.colorMaskChooseBox.addItem("")
        self.colorMaskChooseBox.addItem("")
        self.colorMaskChooseBox.addItem("")
        self.colorMaskChooseBox.addItem("")
        self.colorMaskChooseBox.addItem("")
        self.colorMaskChooseBox.setObjectName(u"colorMaskChooseBox")
        self.colorMaskChooseBox.setGeometry(QRect(110, 50, 201, 22))
        self.pictureChooseButton = QPushButton(self.settingsBox)
        self.pictureChooseButton.setObjectName(u"pictureChooseButton")
        self.pictureChooseButton.setGeometry(QRect(20, 80, 291, 31))
        self.generateButton = QPushButton(self.centralwidget)
        self.generateButton.setObjectName(u"generateButton")
        self.generateButton.setGeometry(QRect(10, 350, 331, 31))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4e8c\u7ef4\u7801\u751f\u6210\u5668",
                                                             None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u7ef4\u7801\u751f\u6210\u5668", None))
        self.inputBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u6587\u672c", None))
        self.settingsBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.drawerChooseLabel.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9Drawer\uff1a", None))
        self.drawerChooseBox.setItemText(0, QCoreApplication.translate("MainWindow", u"CircleModuleDrawer", None))
        self.drawerChooseBox.setItemText(1, QCoreApplication.translate("MainWindow", u"GappedSquareModuleDrawer", None))
        self.drawerChooseBox.setItemText(2, QCoreApplication.translate("MainWindow", u"HorizontalBarsDrawer", None))
        self.drawerChooseBox.setItemText(3, QCoreApplication.translate("MainWindow", u"RoundedModuleDrawer", None))
        self.drawerChooseBox.setItemText(4, QCoreApplication.translate("MainWindow", u"SquareModuleDrawer", None))
        self.drawerChooseBox.setItemText(5, QCoreApplication.translate("MainWindow", u"VerticalBarsDrawer", None))

        self.colorMaskChooseLabel.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9ColorMask\uff1a",
                                                                     None))
        self.colorMaskChooseBox.setItemText(0, QCoreApplication.translate("MainWindow", u"SolidFillColorMask", None))
        self.colorMaskChooseBox.setItemText(1, QCoreApplication.translate("MainWindow", u"RadialGradiantColorMask",
                                                                          None))
        self.colorMaskChooseBox.setItemText(2, QCoreApplication.translate("MainWindow", u"SquareGradiantColorMask",
                                                                          None))
        self.colorMaskChooseBox.setItemText(3, QCoreApplication.translate("MainWindow", u"HorizontalGradiantColorMask",
                                                                          None))
        self.colorMaskChooseBox.setItemText(4, QCoreApplication.translate("MainWindow", u"VerticalGradiantColorMask",
                                                                          None))

        self.pictureChooseButton.setText(QCoreApplication.translate("MainWindow",
                                                                    u"\u9009\u62e9\u7167\u7247\uff08\u53ef\u9009\uff09",
                                                                    None))
        self.generateButton.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210", None))
    # retranslateUi
