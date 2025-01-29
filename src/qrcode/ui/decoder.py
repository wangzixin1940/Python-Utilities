# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'decoder.ui'
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
        MainWindow.resize(347, 221)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(110, 10, 131, 31))
        font = QFont()
        font.setFamilies([u"STZhongsong"])
        font.setPointSize(16)
        self.title.setFont(font)
        self.choosePictureButton = QPushButton(self.centralwidget)
        self.choosePictureButton.setObjectName(u"choosePictureButton")
        self.choosePictureButton.setGeometry(QRect(40, 50, 131, 31))
        self.decodeButton = QPushButton(self.centralwidget)
        self.decodeButton.setObjectName(u"decodeButton")
        self.decodeButton.setGeometry(QRect(190, 50, 131, 31))
        self.resultBox = QGroupBox(self.centralwidget)
        self.resultBox.setObjectName(u"resultBox")
        self.resultBox.setGeometry(QRect(10, 90, 331, 121))
        self.resultDisplay = QTextBrowser(self.resultBox)
        self.resultDisplay.setObjectName(u"resultDisplay")
        self.resultDisplay.setGeometry(QRect(10, 20, 311, 91))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4e8c\u7ef4\u7801\u89e3\u7801\u5668", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u7ef4\u7801\u89e3\u7801\u5668", None))
        self.choosePictureButton.setText(QCoreApplication.translate("MainWindow", u"\u70b9\u8fd9\u91cc\u9009\u62e9\u56fe\u7247", None))
        self.decodeButton.setText(QCoreApplication.translate("MainWindow", u"\u89e3\u7801", None))
        self.resultBox.setTitle(QCoreApplication.translate("MainWindow", u"\u89e3\u7801\u7ed3\u679c", None))
    # retranslateUi

