# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cpd.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(332, 341)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(100, 10, 141, 31))
        font = QFont()
        font.setFamilies([u"FZYaoTi"])
        font.setPointSize(18)
        self.title.setFont(font)
        self.inputLabel = QLabel(self.centralwidget)
        self.inputLabel.setObjectName(u"inputLabel")
        self.inputLabel.setGeometry(QRect(20, 60, 91, 41))
        font1 = QFont()
        font1.setFamilies([u"STZhongsong"])
        font1.setPointSize(11)
        self.inputLabel.setFont(font1)
        self.inputs = QLineEdit(self.centralwidget)
        self.inputs.setObjectName(u"inputs")
        self.inputs.setGeometry(QRect(110, 60, 201, 41))
        self.queryButton = QPushButton(self.centralwidget)
        self.queryButton.setObjectName(u"queryButton")
        self.queryButton.setGeometry(QRect(50, 120, 241, 41))
        self.results = QGroupBox(self.centralwidget)
        self.results.setObjectName(u"results")
        self.results.setGeometry(QRect(20, 170, 301, 161))
        self.pinyinLabel = QLabel(self.results)
        self.pinyinLabel.setObjectName(u"pinyinLabel")
        self.pinyinLabel.setGeometry(QRect(30, 30, 53, 16))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(10)
        self.pinyinLabel.setFont(font2)
        self.zhuyinLabel = QLabel(self.results)
        self.zhuyinLabel.setObjectName(u"zhuyinLabel")
        self.zhuyinLabel.setGeometry(QRect(30, 50, 53, 16))
        self.zhuyinLabel.setFont(font2)
        self.resultPinyin = QLabel(self.results)
        self.resultPinyin.setObjectName(u"resultPinyin")
        self.resultPinyin.setGeometry(QRect(70, 30, 211, 16))
        self.resultZhuyin = QLabel(self.results)
        self.resultZhuyin.setObjectName(u"resultZhuyin")
        self.resultZhuyin.setGeometry(QRect(70, 50, 211, 16))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u6c49\u8bed\u62fc\u97f3\u5b57\u5178", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u6c49\u8bed\u62fc\u97f3\u5b57\u5178", None))
        self.inputLabel.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u4e00\u4e2a\n"
"\u6216\u591a\u4e2a\u6c49\u5b57\uff1a", None))
        self.queryButton.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2", None))
        self.results.setTitle(QCoreApplication.translate("MainWindow", u"\u7ed3\u679c\uff1a", None))
        self.pinyinLabel.setText(QCoreApplication.translate("MainWindow", u"\u62fc\u97f3\uff1a", None))
        self.zhuyinLabel.setText(QCoreApplication.translate("MainWindow", u"\u6ce8\u97f3\uff1a", None))
        self.resultPinyin.setText(QCoreApplication.translate("MainWindow", u"\u672a\u77e5", None))
        self.resultZhuyin.setText(QCoreApplication.translate("MainWindow", u"\u672a\u77e5", None))
    # retranslateUi

