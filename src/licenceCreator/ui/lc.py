# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'lc.ui'
#
# Created by: Qt User Interface Compiler version 6.8.0
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton, QSpinBox, QTabWidget,
                               QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(384, 271)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(10, 10, 181, 31))
        font = QFont()
        font.setFamilies([u"STXihei"])
        font.setPointSize(16)
        self.title.setFont(font)
        self.types = QTabWidget(self.centralwidget)
        self.types.setObjectName(u"types")
        self.types.setGeometry(QRect(0, 40, 381, 171))
        self.apache_tab = QWidget()
        self.apache_tab.setObjectName(u"apache_tab")
        self.nameLabel = QLabel(self.apache_tab)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setGeometry(QRect(0, 10, 101, 21))
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                    Qt.AlignmentFlag.AlignVCenter)
        self.nameEdit = QLineEdit(self.apache_tab)
        self.nameEdit.setObjectName(u"nameEdit")
        self.nameEdit.setGeometry(QRect(100, 10, 271, 21))
        self.yearLabel = QLabel(self.apache_tab)
        self.yearLabel.setObjectName(u"yearLabel")
        self.yearLabel.setGeometry(QRect(0, 40, 101, 21))
        self.yearLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                    Qt.AlignmentFlag.AlignVCenter)
        self.yearEdit = QSpinBox(self.apache_tab)
        self.yearEdit.setObjectName(u"yearEdit")
        self.yearEdit.setGeometry(QRect(100, 40, 271, 22))
        self.types.addTab(self.apache_tab, "")
        self.mit_tab = QWidget()
        self.mit_tab.setObjectName(u"mit_tab")
        self.nameLabel_2 = QLabel(self.mit_tab)
        self.nameLabel_2.setObjectName(u"nameLabel_2")
        self.nameLabel_2.setGeometry(QRect(0, 10, 101, 21))
        self.nameLabel_2.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                      Qt.AlignmentFlag.AlignVCenter)
        self.nameEdit_2 = QLineEdit(self.mit_tab)
        self.nameEdit_2.setObjectName(u"nameEdit_2")
        self.nameEdit_2.setGeometry(QRect(100, 10, 271, 21))
        self.yearLabel_2 = QLabel(self.mit_tab)
        self.yearLabel_2.setObjectName(u"yearLabel_2")
        self.yearLabel_2.setGeometry(QRect(0, 40, 101, 21))
        self.yearLabel_2.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                      Qt.AlignmentFlag.AlignVCenter)
        self.yearEdit_2 = QSpinBox(self.mit_tab)
        self.yearEdit_2.setObjectName(u"yearEdit_2")
        self.yearEdit_2.setGeometry(QRect(100, 40, 271, 22))
        self.types.addTab(self.mit_tab, "")
        self.gpl_tab = QWidget()
        self.gpl_tab.setObjectName(u"gpl_tab")
        self.nameLabel_3 = QLabel(self.gpl_tab)
        self.nameLabel_3.setObjectName(u"nameLabel_3")
        self.nameLabel_3.setGeometry(QRect(0, 10, 101, 21))
        self.nameLabel_3.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                      Qt.AlignmentFlag.AlignVCenter)
        self.yearLabel_3 = QLabel(self.gpl_tab)
        self.yearLabel_3.setObjectName(u"yearLabel_3")
        self.yearLabel_3.setGeometry(QRect(0, 40, 101, 21))
        self.yearLabel_3.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                      Qt.AlignmentFlag.AlignVCenter)
        self.nameEdit_3 = QLineEdit(self.gpl_tab)
        self.nameEdit_3.setObjectName(u"nameEdit_3")
        self.nameEdit_3.setGeometry(QRect(100, 10, 271, 21))
        self.yearEdit_3 = QSpinBox(self.gpl_tab)
        self.yearEdit_3.setObjectName(u"yearEdit_3")
        self.yearEdit_3.setGeometry(QRect(100, 40, 271, 22))
        self.projectNameLabel = QLabel(self.gpl_tab)
        self.projectNameLabel.setObjectName(u"projectNameLabel")
        self.projectNameLabel.setGeometry(QRect(0, 70, 101, 21))
        self.projectNameLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                           Qt.AlignmentFlag.AlignVCenter)
        self.projectNameEdit = QLineEdit(self.gpl_tab)
        self.projectNameEdit.setObjectName(u"projectNameEdit")
        self.projectNameEdit.setGeometry(QRect(100, 70, 271, 21))
        self.projectIntroLabel = QLabel(self.gpl_tab)
        self.projectIntroLabel.setObjectName(u"projectIntroLabel")
        self.projectIntroLabel.setGeometry(QRect(0, 100, 101, 21))
        self.projectIntroLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                            Qt.AlignmentFlag.AlignVCenter)
        self.projectIntroEdit = QLineEdit(self.gpl_tab)
        self.projectIntroEdit.setObjectName(u"projectIntroEdit")
        self.projectIntroEdit.setGeometry(QRect(100, 100, 271, 21))
        self.types.addTab(self.gpl_tab, "")
        self.isc_tab = QWidget()
        self.isc_tab.setObjectName(u"isc_tab")
        self.nameLabel_4 = QLabel(self.isc_tab)
        self.nameLabel_4.setObjectName(u"nameLabel_4")
        self.nameLabel_4.setGeometry(QRect(0, 10, 101, 21))
        self.nameLabel_4.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                      Qt.AlignmentFlag.AlignVCenter)
        self.yearLabel_4 = QLabel(self.isc_tab)
        self.yearLabel_4.setObjectName(u"yearLabel_4")
        self.yearLabel_4.setGeometry(QRect(0, 40, 101, 21))
        self.yearLabel_4.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                      Qt.AlignmentFlag.AlignVCenter)
        self.nameEdit_4 = QLineEdit(self.isc_tab)
        self.nameEdit_4.setObjectName(u"nameEdit_4")
        self.nameEdit_4.setGeometry(QRect(100, 10, 271, 21))
        self.yearEdit_4 = QSpinBox(self.isc_tab)
        self.yearEdit_4.setObjectName(u"yearEdit_4")
        self.yearEdit_4.setGeometry(QRect(100, 40, 271, 22))
        self.types.addTab(self.isc_tab, "")
        self.generateButton = QPushButton(self.centralwidget)
        self.generateButton.setObjectName(u"generateButton")
        self.generateButton.setGeometry(QRect(150, 230, 91, 31))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.types.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u8bb8\u53ef\u8bc1\u521b\u9020\u5668",
                                                             None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"Licence Creator", None))
        self.nameLabel.setText(QCoreApplication.translate("MainWindow",
                                                          u"\u7248\u6743\u6240\u6709\u4eba\u59d3\u540d\uff1a", None))
        # if QT_CONFIG(tooltip)
        self.yearLabel.setToolTip(QCoreApplication.translate("MainWindow",
                                                             u"\u6307\u7248\u6743\u7684\u8d77\u59cb\u5e74\u4efd\uff0c"
                                                             u"\u4f8b\uff1a\n"
                                                             "2025", None))
        # endif // QT_CONFIG(tooltip)
        self.yearLabel.setText(QCoreApplication.translate("MainWindow", u"\u7248\u6743\u5e74\u4efd\uff1a", None))
        self.types.setTabText(self.types.indexOf(self.apache_tab),
                              QCoreApplication.translate("MainWindow", u"Apache 2.0", None))
        self.nameLabel_2.setText(
            QCoreApplication.translate("MainWindow", u"\u7248\u6743\u6240\u6709\u4eba\u59d3\u540d\uff1a", None))
        # if QT_CONFIG(tooltip)
        self.yearLabel_2.setToolTip(QCoreApplication.translate("MainWindow",
                                                               u"\u6307\u7248\u6743\u7684\u8d77\u59cb\u5e74\
                                                               \u4efd\uff0c\u4f8b\uff1a\n"
                                                               "2025", None))
        # endif // QT_CONFIG(tooltip)
        self.yearLabel_2.setText(QCoreApplication.translate("MainWindow", u"\u7248\u6743\u5e74\u4efd\uff1a", None))
        self.types.setTabText(self.types.indexOf(self.mit_tab), QCoreApplication.translate("MainWindow", u"MIT", None))
        self.nameLabel_3.setText(
            QCoreApplication.translate("MainWindow", u"\u7248\u6743\u6240\u6709\u4eba\u59d3\u540d\uff1a", None))
        # if QT_CONFIG(tooltip)
        self.yearLabel_3.setToolTip(QCoreApplication.translate("MainWindow",
                                                               u"\u6307\u7248\u6743\u7684\u8d77\u59cb\u5e74\
                                                               \u4efd\uff0c\u4f8b\uff1a\n"
                                                               "2025", None))
        # endif // QT_CONFIG(tooltip)
        self.yearLabel_3.setText(QCoreApplication.translate("MainWindow", u"\u7248\u6743\u5e74\u4efd\uff1a", None))
        # if QT_CONFIG(tooltip)
        self.projectNameLabel.setToolTip(QCoreApplication.translate("MainWindow",
                                                                    u"\u6307\u7248\u6743\u7684\u8d77\u59cb\u5e74\
                                                                    \u4efd\uff0c\u4f8b\uff1a\n"
                                                                    "2025", None))
        # endif // QT_CONFIG(tooltip)
        self.projectNameLabel.setText(QCoreApplication.translate("MainWindow", u"\u9879\u76ee\u540d\u79f0\uff1a", None))
        # if QT_CONFIG(tooltip)
        self.projectIntroLabel.setToolTip(QCoreApplication.translate("MainWindow",
                                                                     u"\u6307\u7248\u6743\u7684\u8d77\u59cb\u5e74\u4efd\
                                                                     \uff0c\u4f8b\uff1a\n"
                                                                     "2025", None))
        # endif // QT_CONFIG(tooltip)
        self.projectIntroLabel.setText(
            QCoreApplication.translate("MainWindow", u"\u9879\u76ee\u4ecb\u7ecd\uff1a", None))
        self.types.setTabText(self.types.indexOf(self.gpl_tab),
                              QCoreApplication.translate("MainWindow", u"GNU GPL v3", None))
        self.nameLabel_4.setText(
            QCoreApplication.translate("MainWindow", u"\u7248\u6743\u6240\u6709\u4eba\u59d3\u540d\uff1a", None))
        # if QT_CONFIG(tooltip)
        self.yearLabel_4.setToolTip(QCoreApplication.translate("MainWindow",
                                                               u"\u6307\u7248\u6743\u7684\u8d77\u59cb\
                                                               \u5e74\u4efd\uff0c\u4f8b\uff1a\n"
                                                               "2025", None))
        # endif // QT_CONFIG(tooltip)
        self.yearLabel_4.setText(QCoreApplication.translate("MainWindow", u"\u7248\u6743\u5e74\u4efd\uff1a", None))
        self.types.setTabText(self.types.indexOf(self.isc_tab), QCoreApplication.translate("MainWindow", u"ISC", None))
        self.generateButton.setText(QCoreApplication.translate("MainWindow", u"\u521b\u9020", None))
    # retranslateUi
