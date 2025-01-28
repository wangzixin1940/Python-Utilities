# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'photo.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 325)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 280, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.title = QLabel(Dialog)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(10, 10, 81, 21))
        font = QFont()
        font.setFamilies([u"STZhongsong"])
        font.setPointSize(14)
        self.title.setFont(font)
        self.photoDisplay = QLabel(Dialog)
        self.photoDisplay.setObjectName(u"photoDisplay")
        self.photoDisplay.setGeometry(QRect(10, 40, 381, 171))
        font1 = QFont()
        font1.setFamilies([u"STZhongsong"])
        font1.setPointSize(26)
        self.photoDisplay.setFont(font1)
        self.photoDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.takePhotoButton = QPushButton(Dialog)
        self.takePhotoButton.setObjectName(u"takePhotoButton")
        self.takePhotoButton.setGeometry(QRect(10, 223, 381, 51))
        font2 = QFont()
        font2.setPointSize(12)
        self.takePhotoButton.setFont(font2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u62cd\u7167\u8bc6\u522b", None))
        self.title.setText(QCoreApplication.translate("Dialog", u"\u62cd\u7167\u8bc6\u522b", None))
        self.photoDisplay.setText(QCoreApplication.translate("Dialog", u"\u73b0\u5728\u62cd\u7167", None))
        self.takePhotoButton.setText(QCoreApplication.translate("Dialog", u"\u62cd\u7167", None))
    # retranslateUi

