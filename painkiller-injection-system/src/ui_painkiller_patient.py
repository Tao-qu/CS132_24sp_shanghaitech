# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'painkiller_patientUBAnZf.ui'
##
# Created by: Qt User Interface Compiler version 5.14.1
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
                          QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                         QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
                         QRadialGradient)
from PyQt5.QtWidgets import *


class Ui_Dialog_Patient(object):
    def setupUi(self, Dialog_Patient):
        if Dialog_Patient.objectName():
            Dialog_Patient.setObjectName(u"Dialog_Patient")
        Dialog_Patient.resize(461, 208)
        self.label_5 = QLabel(Dialog_Patient)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 70, 331, 41))
        font = QFont()
        font.setFamily(u"Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.InjectionButtom_2 = QPushButton(Dialog_Patient)
        self.InjectionButtom_2.setObjectName(u"InjectionButtom_2")
        self.InjectionButtom_2.setGeometry(QRect(10, 130, 101, 23))
        self.label = QLabel(Dialog_Patient)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 381, 51))
        font1 = QFont()
        font1.setFamily(u"Alimama ShuHeiTi Bold")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.label.setFont(font1)

        self.retranslateUi(Dialog_Patient)

        QMetaObject.connectSlotsByName(Dialog_Patient)
    # setupUi

    def retranslateUi(self, Dialog_Patient):
        Dialog_Patient.setWindowTitle(
            QCoreApplication.translate("Dialog_Patient", u"Dialog", None))
        self.label_5.setText(QCoreApplication.translate(
            "Dialog_Patient", u"Request Botton", None))
        self.InjectionButtom_2.setText(QCoreApplication.translate(
            "Dialog_Patient", u"RequestBolus", None))
        self.label.setText(QCoreApplication.translate(
            "Dialog_Patient", u"Painkiller Injection: Patient", None))
    # retranslateUi
