# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ocr.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QTextBrowser, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(298, 354)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(100, 20, 111, 31))
        font = QFont()
        font.setFamilies([u"STZhongsong"])
        font.setPointSize(16)
        self.title.setFont(font)
        self.choosePictureButton = QPushButton(self.centralwidget)
        self.choosePictureButton.setObjectName(u"choosePictureButton")
        self.choosePictureButton.setGeometry(QRect(90, 60, 131, 31))
        self.identifyButton = QPushButton(self.centralwidget)
        self.identifyButton.setObjectName(u"identifyButton")
        self.identifyButton.setGeometry(QRect(90, 110, 131, 31))
        self.resultDisplayBox = QGroupBox(self.centralwidget)
        self.resultDisplayBox.setObjectName(u"resultDisplayBox")
        self.resultDisplayBox.setGeometry(QRect(10, 150, 281, 201))
        self.resultDisplay = QTextBrowser(self.resultDisplayBox)
        self.resultDisplay.setObjectName(u"resultDisplay")
        self.resultDisplay.setGeometry(QRect(10, 20, 256, 171))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u6587\u5b57\u8bc6\u522b\u5668", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u6587\u5b57\u8bc6\u522b\u5668", None))
        self.choosePictureButton.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u7167\u7247\u6216\u62cd\u7167", None))
        self.identifyButton.setText(QCoreApplication.translate("MainWindow", u"\u8bc6\u522b", None))
        self.resultDisplayBox.setTitle(QCoreApplication.translate("MainWindow", u"\u7ed3\u679c", None))
    # retranslateUi

