# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'amk.ui'
#
# Created by: Qt User Interface Compiler version 6.8.0
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialogButtonBox, QLabel, QPushButton


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 170)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(290, 20, 81, 131))
        self.buttonBox.setOrientation(Qt.Orientation.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close | QDialogButtonBox.StandardButton.Help)
        self.title = QLabel(Dialog)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(10, 10, 101, 31))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        self.title.setFont(font)
        self.choose_file = QPushButton(Dialog)
        self.choose_file.setObjectName(u"choose_file")
        self.choose_file.setGeometry(QRect(10, 50, 261, 51))
        self.run_script = QPushButton(Dialog)
        self.run_script.setObjectName(u"run_script")
        self.run_script.setGeometry(QRect(10, 110, 261, 51))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Auto Mouse and Keyboard App", None))
        # if QT_CONFIG(tooltip)
        self.title.setToolTip(QCoreApplication.translate("Dialog", u"Auto Mouse and Keyboard App\n"
                                                                   "\u81ea\u52a8\u7ba1\u7406\u60a8\u7684\
                                                                   \u9f20\u6807\u548c\u952e\u76d8\u64cd\u4f5c\
                                                                   \uff0c\u53ea\u7528\u5199\u4e00\u4e2a\u7b80\
                                                                   \u5355\u7684\u5b8f\u3002", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(whatsthis)
        self.title.setWhatsThis("")
        # endif // QT_CONFIG(whatsthis)
        self.title.setText(QCoreApplication.translate("Dialog", u"AMK App", None))
        self.choose_file.setText(QCoreApplication.translate("Dialog",
                                                            u"\u70b9\u51fb\u8fd9\u4e2a\u6309\u94ae\uff0c"
                                                            u"\u9009\u62e9\u60a8\u7684\u5b8f\u6587\u4ef6",
                                                            None))
        self.run_script.setText(
            QCoreApplication.translate("Dialog", u"\u8fd0\u884c\u60a8\u7684\u5b8f\u6587\u4ef6", None))
    # retranslateUi
