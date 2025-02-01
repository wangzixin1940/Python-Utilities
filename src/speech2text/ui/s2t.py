# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 's2t.ui'
#
# Created by: Qt User Interface Compiler version 6.8.0
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QComboBox, QLabel, QPushButton, QTextBrowser, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(336, 350)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(120, 10, 111, 21))
        font = QFont()
        font.setFamilies([u"STZhongsong"])
        font.setPointSize(16)
        self.title.setFont(font)
        self.modelChooseLabel = QLabel(self.centralwidget)
        self.modelChooseLabel.setObjectName(u"modelChooseLabel")
        self.modelChooseLabel.setGeometry(QRect(20, 50, 61, 21))
        self.modelChooseCombo = QComboBox(self.centralwidget)
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.addItem("")
        self.modelChooseCombo.setObjectName(u"modelChooseCombo")
        self.modelChooseCombo.setGeometry(QRect(80, 50, 231, 22))
        self.uploadAudioButton = QPushButton(self.centralwidget)
        self.uploadAudioButton.setObjectName(u"uploadAudioButton")
        self.uploadAudioButton.setGeometry(QRect(20, 80, 291, 31))
        self.identifyButton = QPushButton(self.centralwidget)
        self.identifyButton.setObjectName(u"identifyButton")
        self.identifyButton.setGeometry(QRect(20, 120, 291, 31))
        self.resultDisplay = QTextBrowser(self.centralwidget)
        self.resultDisplay.setObjectName(u"resultDisplay")
        self.resultDisplay.setGeometry(QRect(20, 160, 291, 181))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u8bed\u97f3\u8f6c\u6587\u5b57", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u8bed\u97f3\u8f6c\u6587\u5b57", None))
        self.modelChooseLabel.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6a21\u578b\uff1a", None))
        self.modelChooseCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"vosk-model-small-en-us-0.15",
                                                                        None))
        self.modelChooseCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"vosk-model-en-us-0.22", None))
        self.modelChooseCombo.setItemText(2, QCoreApplication.translate("MainWindow", u"vosk-model-en-us-0.22-lgraph",
                                                                        None))
        self.modelChooseCombo.setItemText(3,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-en-us-0.42-gigaspeech",
                                                                     None))
        self.modelChooseCombo.setItemText(4,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-en-us-daanzu-20200905",
                                                                     None))
        self.modelChooseCombo.setItemText(5, QCoreApplication.translate("MainWindow",
                                                                        u"vosk-model-en-us-daanzu-20200905-lgraph",
                                                                        None))
        self.modelChooseCombo.setItemText(6,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-en-us-librispeech-0.2",
                                                                     None))
        self.modelChooseCombo.setItemText(7,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-en-us-zamia-0.5",
                                                                     None))
        self.modelChooseCombo.setItemText(8, QCoreApplication.translate("MainWindow", u"vosk-model-en-us-aspire-0.2",
                                                                        None))
        self.modelChooseCombo.setItemText(9, QCoreApplication.translate("MainWindow", u"vosk-model-en-us-0.21", None))
        self.modelChooseCombo.setItemText(10, QCoreApplication.translate("MainWindow", u"vosk-model-en-in-0.5", None))
        self.modelChooseCombo.setItemText(11,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-en-in-0.4", None))
        self.modelChooseCombo.setItemText(12,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-cn-0.22", None))
        self.modelChooseCombo.setItemText(13, QCoreApplication.translate("MainWindow", u"vosk-model-cn-0.22", None))
        self.modelChooseCombo.setItemText(14,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-cn-kaldi-multicn-0.15",
                                                                     None))
        self.modelChooseCombo.setItemText(15, QCoreApplication.translate("MainWindow", u"vosk-model-ru-0.42", None))
        self.modelChooseCombo.setItemText(16,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-ru-0.22", None))
        self.modelChooseCombo.setItemText(17, QCoreApplication.translate("MainWindow", u"vosk-model-ru-0.22", None))
        self.modelChooseCombo.setItemText(18, QCoreApplication.translate("MainWindow", u"vosk-model-ru-0.10", None))
        self.modelChooseCombo.setItemText(19,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-fr-0.22", None))
        self.modelChooseCombo.setItemText(20, QCoreApplication.translate("MainWindow", u"vosk-model-fr-0.22", None))
        self.modelChooseCombo.setItemText(21,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-fr-pguyot-0.3",
                                                                     None))
        self.modelChooseCombo.setItemText(22, QCoreApplication.translate("MainWindow", u"vosk-model-fr-0.6-linto-2.2.0",
                                                                         None))
        self.modelChooseCombo.setItemText(23, QCoreApplication.translate("MainWindow", u"vosk-model-de-0.21", None))
        self.modelChooseCombo.setItemText(24, QCoreApplication.translate("MainWindow", u"vosk-model-de-tuda-0.6-900k",
                                                                         None))
        self.modelChooseCombo.setItemText(25, QCoreApplication.translate("MainWindow", u"vosk-model-small-de-zamia-0.3",
                                                                         None))
        self.modelChooseCombo.setItemText(26,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-de-0.15", None))
        self.modelChooseCombo.setItemText(27,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-es-0.42", None))
        self.modelChooseCombo.setItemText(28, QCoreApplication.translate("MainWindow", u"vosk-model-es-0.42", None))
        self.modelChooseCombo.setItemText(29,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-pt-0.3", None))
        self.modelChooseCombo.setItemText(30, QCoreApplication.translate("MainWindow",
                                                                         u"vosk-model-pt-fb-v0.1.1-20220516_2113",
                                                                         None))
        self.modelChooseCombo.setItemText(31, QCoreApplication.translate("MainWindow", u"vosk-model-el-gr-0.7", None))
        self.modelChooseCombo.setItemText(32,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-tr-0.3", None))
        self.modelChooseCombo.setItemText(33,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-vn-0.4", None))
        self.modelChooseCombo.setItemText(34, QCoreApplication.translate("MainWindow", u"vosk-model-vn-0.4", None))
        self.modelChooseCombo.setItemText(35,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-it-0.22", None))
        self.modelChooseCombo.setItemText(36, QCoreApplication.translate("MainWindow", u"vosk-model-it-0.22", None))
        self.modelChooseCombo.setItemText(37,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-nl-0.22", None))
        self.modelChooseCombo.setItemText(38, QCoreApplication.translate("MainWindow",
                                                                         u"vosk-model-nl-spraakherkenning-0.6", None))
        self.modelChooseCombo.setItemText(39, QCoreApplication.translate("MainWindow",
                                                                         u"vosk-model-nl-spraakherkenning-0.6-lgraph",
                                                                         None))
        self.modelChooseCombo.setItemText(40,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-ca-0.4", None))
        self.modelChooseCombo.setItemText(41, QCoreApplication.translate("MainWindow", u"vosk-model-ar-mgb2-0.4", None))
        self.modelChooseCombo.setItemText(42,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-ar-0.22-linto-1.1.0",
                                                                     None))
        self.modelChooseCombo.setItemText(43,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-fa-0.4", None))
        self.modelChooseCombo.setItemText(44, QCoreApplication.translate("MainWindow", u"vosk-model-fa-0.5", None))
        self.modelChooseCombo.setItemText(45,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-fa-0.5", None))
        self.modelChooseCombo.setItemText(46, QCoreApplication.translate("MainWindow", u"vosk-model-tl-ph-generic-0.6",
                                                                         None))
        self.modelChooseCombo.setItemText(47, QCoreApplication.translate("MainWindow", u"vosk-model-small-uk-v3-nano",
                                                                         None))
        self.modelChooseCombo.setItemText(48, QCoreApplication.translate("MainWindow", u"vosk-model-small-uk-v3-small",
                                                                         None))
        self.modelChooseCombo.setItemText(49, QCoreApplication.translate("MainWindow", u"vosk-model-uk-v3", None))
        self.modelChooseCombo.setItemText(50,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-uk-v3-lgraph", None))
        self.modelChooseCombo.setItemText(51,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-kz-0.15", None))
        self.modelChooseCombo.setItemText(52, QCoreApplication.translate("MainWindow", u"vosk-model-kz-0.15", None))
        self.modelChooseCombo.setItemText(53,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-sv-rhasspy-0.15",
                                                                     None))
        self.modelChooseCombo.setItemText(54,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-ja-0.22", None))
        self.modelChooseCombo.setItemText(55, QCoreApplication.translate("MainWindow", u"vosk-model-ja-0.22", None))
        self.modelChooseCombo.setItemText(56,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-eo-0.42", None))
        self.modelChooseCombo.setItemText(57,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-hi-0.22", None))
        self.modelChooseCombo.setItemText(58, QCoreApplication.translate("MainWindow", u"vosk-model-hi-0.22", None))
        self.modelChooseCombo.setItemText(59,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-cs-0.4-rhasspy",
                                                                     None))
        self.modelChooseCombo.setItemText(60,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-pl-0.22", None))
        self.modelChooseCombo.setItemText(61,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-uz-0.22", None))
        self.modelChooseCombo.setItemText(62,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-ko-0.22", None))
        self.modelChooseCombo.setItemText(63, QCoreApplication.translate("MainWindow", u"vosk-model-br-0.8", None))
        self.modelChooseCombo.setItemText(64, QCoreApplication.translate("MainWindow", u"vosk-model-gu-0.42", None))
        self.modelChooseCombo.setItemText(65,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-gu-0.42", None))
        self.modelChooseCombo.setItemText(66, QCoreApplication.translate("MainWindow", u"vosk-model-tg-0.22", None))
        self.modelChooseCombo.setItemText(67,
                                          QCoreApplication.translate("MainWindow", u"vosk-model-small-tg-0.22", None))
        self.modelChooseCombo.setItemText(68, QCoreApplication.translate("MainWindow", u"vosk-model-spk-0.4", None))
        self.modelChooseCombo.setItemText(69,
                                          QCoreApplication.translate("MainWindow", u"vosk-recasepunc-en-0.22", None))
        self.modelChooseCombo.setItemText(70,
                                          QCoreApplication.translate("MainWindow", u"vosk-recasepunc-ru-0.22", None))
        self.modelChooseCombo.setItemText(71,
                                          QCoreApplication.translate("MainWindow", u"vosk-recasepunc-de-0.21", None))

        self.uploadAudioButton.setText(
            QCoreApplication.translate("MainWindow", u"\u4e0a\u4f20\u60a8\u7684\u5f55\u97f3", None))
        self.identifyButton.setText(QCoreApplication.translate("MainWindow", u"\u8bc6\u522b\u6587\u5b57", None))
    # retranslateUi
