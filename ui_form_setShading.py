# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QSpacerItem


class Ui_setShading(object):
    def setupUi(self, setShading):
        if not setShading.objectName():
            setShading.setObjectName(u"setShading")
        setShading.resize(181, 269)
        setShading.setMinimumSize(QSize(181, 269))
        setShading.setMaximumSize(QSize(181, 269))
        self.gridLayout_2 = QGridLayout(setShading)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_6 = QLabel(setShading)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.pushButton_setShading = QPushButton(setShading)
        self.pushButton_setShading.setObjectName(u"pushButton_setShading")

        self.gridLayout.addWidget(self.pushButton_setShading, 6, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)

        self.lineEdit_altitude = QLineEdit(setShading)
        self.lineEdit_altitude.setObjectName(u"lineEdit_altitude")

        self.gridLayout.addWidget(self.lineEdit_altitude, 2, 1, 1, 1)

        self.label_2 = QLabel(setShading)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 2,
                                  Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.lineEdit_vert_exag = QLineEdit(setShading)
        self.lineEdit_vert_exag.setObjectName(u"lineEdit_vert_exag")

        self.gridLayout.addWidget(self.lineEdit_vert_exag, 5, 1, 1, 1)

        self.label_5 = QLabel(setShading)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)

        self.label_3 = QLabel(setShading)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_4 = QLabel(setShading)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.lineEdit_azimuth = QLineEdit(setShading)
        self.lineEdit_azimuth.setObjectName(u"lineEdit_azimuth")

        self.gridLayout.addWidget(self.lineEdit_azimuth, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 2)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(setShading)

        QMetaObject.connectSlotsByName(setShading)

    # setupUi

    def retranslateUi(self, setShading):
        setShading.setWindowTitle(QCoreApplication.translate("setShading", u"Set Shading", None))
        self.label_6.setText(QCoreApplication.translate("setShading", u"vert_exag:", None))
        self.pushButton_setShading.setText(QCoreApplication.translate("setShading", u"Set Shading", None))
        self.label_2.setText(QCoreApplication.translate("setShading", u"Light Source position \n"
                                                                      "(in deg):", None))
        self.label_5.setText(QCoreApplication.translate("setShading", u"Exaggeration of elevation:", None))
        self.label_3.setText(QCoreApplication.translate("setShading", u"Azimuth:", None))
        self.label_4.setText(QCoreApplication.translate("setShading", u"Altitude:", None))
    # retranslateUi
