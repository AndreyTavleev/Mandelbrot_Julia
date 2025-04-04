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


class Ui_setC(object):
    def setupUi(self, setC):
        if not setC.objectName():
            setC.setObjectName(u"setC")
        setC.resize(272, 329)
        setC.setMinimumSize(QSize(272, 329))
        setC.setMaximumSize(QSize(272, 329))
        self.gridLayout = QGridLayout(setC)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_setC = QGridLayout()
        self.gridLayout_setC.setObjectName(u"gridLayout_setC")
        self.lineEdit_rhoC = QLineEdit(setC)
        self.lineEdit_rhoC.setObjectName(u"lineEdit_rhoC")

        self.gridLayout_setC.addWidget(self.lineEdit_rhoC, 5, 2, 1, 1)

        self.lineEdit_phiC = QLineEdit(setC)
        self.lineEdit_phiC.setObjectName(u"lineEdit_phiC")

        self.gridLayout_setC.addWidget(self.lineEdit_phiC, 6, 2, 1, 1)

        self.lineEdit_ReC = QLineEdit(setC)
        self.lineEdit_ReC.setObjectName(u"lineEdit_ReC")

        self.gridLayout_setC.addWidget(self.lineEdit_ReC, 1, 2, 1, 1)

        self.label_rhoC = QLabel(setC)
        self.label_rhoC.setObjectName(u"label_rhoC")

        self.gridLayout_setC.addWidget(self.label_rhoC, 5, 1, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_setC.addItem(self.horizontalSpacer_4, 6, 3, 1, 1)

        self.label_3 = QLabel(setC)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_setC.addWidget(self.label_3, 1, 1, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.horizontalSpacer = QSpacerItem(30, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_setC.addItem(self.horizontalSpacer, 1, 3, 1, 1)

        self.label_4 = QLabel(setC)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_setC.addWidget(self.label_4, 2, 1, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_phiC = QLabel(setC)
        self.label_phiC.setObjectName(u"label_phiC")

        self.gridLayout_setC.addWidget(self.label_phiC, 6, 1, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_setC.addItem(self.horizontalSpacer_2, 2, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_setC.addItem(self.horizontalSpacer_3, 5, 3, 1, 1)

        self.lineEdit_ImC = QLineEdit(setC)
        self.lineEdit_ImC.setObjectName(u"lineEdit_ImC")

        self.gridLayout_setC.addWidget(self.lineEdit_ImC, 2, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(21, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_setC.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_setC.addItem(self.horizontalSpacer_6, 2, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_setC.addItem(self.horizontalSpacer_7, 5, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_setC.addItem(self.horizontalSpacer_8, 6, 0, 1, 1)

        self.pushButton_RhoPhiC = QPushButton(setC)
        self.pushButton_RhoPhiC.setObjectName(u"pushButton_RhoPhiC")

        self.gridLayout_setC.addWidget(self.pushButton_RhoPhiC, 7, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter)

        self.pushButto_ReImC = QPushButton(setC)
        self.pushButto_ReImC.setObjectName(u"pushButto_ReImC")

        self.gridLayout_setC.addWidget(self.pushButto_ReImC, 3, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter)

        self.label_2 = QLabel(setC)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_setC.addWidget(self.label_2, 4, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter)

        self.label = QLabel(setC)
        self.label.setObjectName(u"label")

        self.gridLayout_setC.addWidget(self.label, 0, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter)

        self.gridLayout.addLayout(self.gridLayout_setC, 0, 0, 1, 1)

        self.retranslateUi(setC)

        QMetaObject.connectSlotsByName(setC)

    # setupUi

    def retranslateUi(self, setC):
        setC.setWindowTitle(QCoreApplication.translate("setC", u"Set C", None))
        self.label_rhoC.setText(QCoreApplication.translate("setC", u"Modulus, rho:", None))
        self.label_3.setText(QCoreApplication.translate("setC", u"Re(C):", None))
        self.label_4.setText(QCoreApplication.translate("setC", u"Im(C):", None))
        self.label_phiC.setText(QCoreApplication.translate("setC", u"Argument, phi:", None))
        self.pushButton_RhoPhiC.setText(QCoreApplication.translate("setC", u"Set rho and phi", None))
        self.pushButto_ReImC.setText(QCoreApplication.translate("setC", u"Set Re(C) and Im(C)", None))
        self.label_2.setText(QCoreApplication.translate("setC", u"Or set the modulus and argument:", None))
        self.label.setText(QCoreApplication.translate("setC", u"Set the Real and Imaginary parts of C:", None))
    # retranslateUi
