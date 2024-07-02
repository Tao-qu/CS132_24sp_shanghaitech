# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'painkillerUVdERP.ui'
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(925, 723)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 50, 771, 41))
        font = QFont()
        font.setFamily(u"Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 224, 741, 31))
        self.label_3.setFont(font)
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, -10, 611, 71))
        font1 = QFont()
        font1.setFamily(u"Alimama ShuHeiTi Bold")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.label_4.setFont(font1)
        self.progress_1h = QProgressBar(Dialog)
        self.progress_1h.setObjectName(u"progress_1h")
        self.progress_1h.setGeometry(QRect(20, 394, 118, 23))
        self.progress_1h.setValue(24)
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 344, 641, 31))
        self.label_6.setFont(font)
        self.progress_24h = QProgressBar(Dialog)
        self.progress_24h.setObjectName(u"progress_24h")
        self.progress_24h.setGeometry(QRect(180, 394, 118, 23))
        self.progress_24h.setValue(24)
        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(20, 159, 181, 31))
        self.label_7.setFont(font)
        self.StartBaselineBottom = QPushButton(Dialog)
        self.StartBaselineBottom.setObjectName(u"StartBaselineBottom")
        self.StartBaselineBottom.setGeometry(QRect(20, 194, 75, 23))
        self.RstButton = QPushButton(Dialog)
        self.RstButton.setObjectName(u"RstButton")
        self.RstButton.setGeometry(QRect(20, 434, 75, 23))
        self.lcdNumber = QLCDNumber(Dialog)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setGeometry(QRect(20, 515, 64, 23))
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 470, 531, 31))
        self.label_5.setFont(font)
        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(100, 515, 41, 31))
        font2 = QFont()
        font2.setFamily(u"Alimama ShuHeiTi Bold")
        font2.setPointSize(9)
        font2.setBold(True)
        font2.setWeight(75)
        self.label_8.setFont(font2)
        self.lcdNumber_2 = QLCDNumber(Dialog)
        self.lcdNumber_2.setObjectName(u"lcdNumber_2")
        self.lcdNumber_2.setGeometry(QRect(160, 515, 64, 23))
        self.label_9 = QLabel(Dialog)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(240, 515, 51, 31))
        self.label_9.setFont(font2)
        self.lcdNumber_3 = QLCDNumber(Dialog)
        self.lcdNumber_3.setObjectName(u"lcdNumber_3")
        self.lcdNumber_3.setGeometry(QRect(300, 515, 64, 23))
        self.label_10 = QLabel(Dialog)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(380, 505, 141, 51))
        self.label_10.setFont(font2)
        self.horizontalSlider = QSlider(Dialog)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(20, 100, 261, 21))
        self.horizontalSlider.setMinimum(10)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider_2 = QSlider(Dialog)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setGeometry(QRect(20, 274, 261, 21))
        self.horizontalSlider_2.setMinimum(200)
        self.horizontalSlider_2.setMaximum(500)
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)
        self.label_11 = QLabel(Dialog)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(20, 130, 181, 31))
        font3 = QFont()
        font3.setFamily(u"Cambria")
        font3.setPointSize(8)
        self.label_11.setFont(font3)
        self.label_12 = QLabel(Dialog)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(20, 304, 321, 31))
        self.label_12.setFont(font3)
        self.switchlabel = QLabel(Dialog)
        self.switchlabel.setObjectName(u"switchlabel")
        self.switchlabel.setGeometry(QRect(220, 189, 271, 31))
        font4 = QFont()
        font4.setFamily(u"Cambria")
        self.switchlabel.setFont(font4)
        self.baselinelabel = QLabel(Dialog)
        self.baselinelabel.setObjectName(u"baselinelabel")
        self.baselinelabel.setGeometry(QRect(220, 174, 241, 16))
        self.baselinelabel.setFont(font4)
        self.timeadjustdial = QDial(Dialog)
        self.timeadjustdial.setObjectName(u"timeadjustdial")
        self.timeadjustdial.setGeometry(QRect(20, 631, 50, 64))
        self.timeadjustdial.setMinimum(0)
        self.timeadjustdial.setMaximum(60)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 570, 341, 51))
        self.label_2.setFont(font)
        self.timeadjustlabel = QLabel(Dialog)
        self.timeadjustlabel.setObjectName(u"timeadjustlabel")
        self.timeadjustlabel.setGeometry(QRect(100, 640, 481, 41))
        self.timeadjustlabel.setFont(font4)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate(
            "Dialog", u"Adjust Baseline Amount(0.01-0.1ml/min)", None))
        self.label_3.setText(QCoreApplication.translate(
            "Dialog", u"Set Bolus Amount(0.2-0.5ml/shot)", None))
        self.label_4.setText(QCoreApplication.translate(
            "Dialog", u"Painkiller Injection: Physician", None))
        self.label_6.setText(QCoreApplication.translate(
            "Dialog", u"Injection Limit Process", None))
        self.label_7.setText(QCoreApplication.translate(
            "Dialog", u"Baseline State", None))
        self.StartBaselineBottom.setText(
            QCoreApplication.translate("Dialog", u"Switch", None))
        self.RstButton.setText(
            QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_5.setText(QCoreApplication.translate(
            "Dialog", u"Time Display", None))
        self.label_8.setText(
            QCoreApplication.translate("Dialog", u"Days", None))
        self.label_9.setText(
            QCoreApplication.translate("Dialog", u"Hours", None))
        self.label_10.setText(
            QCoreApplication.translate("Dialog", u"Minutes", None))
        self.label_11.setText(QCoreApplication.translate(
            "Dialog", u"Current Baseline: 0.01", None))
        self.label_12.setText(QCoreApplication.translate(
            "Dialog", u"Current Bolus: 0.2", None))
        self.switchlabel.setText(QCoreApplication.translate(
            "Dialog", u"The switch is off.", None))
        self.baselinelabel.setText(QCoreApplication.translate(
            "Dialog", u"Baseline: off", None))
        self.label_2.setText(QCoreApplication.translate(
            "Dialog", u"Time Speed Adjust", None))
        self.timeadjustlabel.setText(QCoreApplication.translate(
            "Dialog", u"Current time speed: 0.5min/s.", None))
    # retranslateUi
