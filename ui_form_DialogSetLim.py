# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QGridLayout, QLabel, QLineEdit, QPushButton,
                               QSizePolicy, QSpacerItem, QVBoxLayout)


class Ui_SetLimits(object):
    def setupUi(self, SetLimits):
        if not SetLimits.objectName():
            SetLimits.setObjectName(u"SetLimits")
        SetLimits.resize(440, 399)
        SetLimits.setMinimumSize(QSize(440, 399))
        SetLimits.setMaximumSize(QSize(16777215, 399))
        self.gridLayout = QGridLayout(SetLimits)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(SetLimits)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.gridLayout_limXY = QGridLayout()
        self.gridLayout_limXY.setObjectName(u"gridLayout_limXY")
        self.label_X = QLabel(SetLimits)
        self.label_X.setObjectName(u"label_X")

        self.gridLayout_limXY.addWidget(self.label_X, 0, 0, 1, 1)

        self.lineEdit_X = QLineEdit(SetLimits)
        self.lineEdit_X.setObjectName(u"lineEdit_X")

        self.gridLayout_limXY.addWidget(self.lineEdit_X, 0, 1, 1, 1)

        self.label_Y = QLabel(SetLimits)
        self.label_Y.setObjectName(u"label_Y")

        self.gridLayout_limXY.addWidget(self.label_Y, 1, 0, 1, 1)

        self.lineEdit_Y = QLineEdit(SetLimits)
        self.lineEdit_Y.setObjectName(u"lineEdit_Y")

        self.gridLayout_limXY.addWidget(self.lineEdit_Y, 1, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout_limXY)

        self.pushButton_SetLim = QPushButton(SetLimits)
        self.pushButton_SetLim.setObjectName(u"pushButton_SetLim")

        self.verticalLayout.addWidget(self.pushButton_SetLim, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_2 = QLabel(SetLimits)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.gridLayout_C = QGridLayout()
        self.gridLayout_C.setObjectName(u"gridLayout_C")
        self.lineEdit_YC = QLineEdit(SetLimits)
        self.lineEdit_YC.setObjectName(u"lineEdit_YC")

        self.gridLayout_C.addWidget(self.lineEdit_YC, 1, 2, 1, 1)

        self.lineEdit_deltaY = QLineEdit(SetLimits)
        self.lineEdit_deltaY.setObjectName(u"lineEdit_deltaY")

        self.gridLayout_C.addWidget(self.lineEdit_deltaY, 3, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(90, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_C.addItem(self.horizontalSpacer, 0, 0, 4, 1)

        self.lineEdit_deltaX = QLineEdit(SetLimits)
        self.lineEdit_deltaX.setObjectName(u"lineEdit_deltaX")

        self.gridLayout_C.addWidget(self.lineEdit_deltaX, 2, 2, 1, 1)

        self.label_deltaX = QLabel(SetLimits)
        self.label_deltaX.setObjectName(u"label_deltaX")

        self.gridLayout_C.addWidget(self.label_deltaX, 2, 1, 1, 1)

        self.lineEdit_XC = QLineEdit(SetLimits)
        self.lineEdit_XC.setObjectName(u"lineEdit_XC")

        self.gridLayout_C.addWidget(self.lineEdit_XC, 0, 2, 1, 1)

        self.label_YC = QLabel(SetLimits)
        self.label_YC.setObjectName(u"label_YC")

        self.gridLayout_C.addWidget(self.label_YC, 1, 1, 1, 1)

        self.label_XC = QLabel(SetLimits)
        self.label_XC.setObjectName(u"label_XC")

        self.gridLayout_C.addWidget(self.label_XC, 0, 1, 1, 1)

        self.label_deltaY = QLabel(SetLimits)
        self.label_deltaY.setObjectName(u"label_deltaY")

        self.gridLayout_C.addWidget(self.label_deltaY, 3, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(90, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_C.addItem(self.horizontalSpacer_2, 0, 3, 4, 1)

        self.verticalLayout.addLayout(self.gridLayout_C)

        self.pushButton_SetC = QPushButton(SetLimits)
        self.pushButton_SetC.setObjectName(u"pushButton_SetC")

        self.verticalLayout.addWidget(self.pushButton_SetC, 0, Qt.AlignmentFlag.AlignHCenter)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(SetLimits)

        QMetaObject.connectSlotsByName(SetLimits)

    # setupUi

    def retranslateUi(self, SetLimits):
        SetLimits.setWindowTitle(QCoreApplication.translate("SetLimits", u"Set Limits", None))
        self.label.setText(QCoreApplication.translate("SetLimits", u"Set the X-axis and Y-axis limits:", None))
        self.label_X.setText(QCoreApplication.translate("SetLimits", u"Xmin, Xmax:", None))
        self.label_Y.setText(QCoreApplication.translate("SetLimits", u"Ymin, Ymax:", None))
        self.pushButton_SetLim.setText(QCoreApplication.translate("SetLimits", u"Set limits", None))
        self.label_2.setText(QCoreApplication.translate("SetLimits", u"Or set coordinates of the centre \n"
                                                                     "and the width of the X-axis and Y-axis:", None))
        self.label_deltaX.setText(QCoreApplication.translate("SetLimits", u"deltaX:", None))
        self.label_YC.setText(QCoreApplication.translate("SetLimits", u"YCentre:", None))
        self.label_XC.setText(QCoreApplication.translate("SetLimits", u"XCentre:", None))
        self.label_deltaY.setText(QCoreApplication.translate("SetLimits", u"deltaY:", None))
        self.pushButton_SetC.setText(QCoreApplication.translate("SetLimits", u"Set centre", None))
    # retranslateUi
