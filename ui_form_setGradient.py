# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget


class Ui_setGradient(object):
    def setupUi(self, setGradient):
        if not setGradient.objectName():
            setGradient.setObjectName(u"setGradient")
        setGradient.resize(421, 210)
        setGradient.setMinimumSize(QSize(421, 210))
        setGradient.setMaximumSize(QSize(421, 210))
        self.gridLayout_2 = QGridLayout(setGradient)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(setGradient)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter)

        self.pushButton_Load = QPushButton(setGradient)
        self.pushButton_Load.setObjectName(u"pushButton_Load")

        self.gridLayout.addWidget(self.pushButton_Load, 3, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.pushButton_Apply = QPushButton(setGradient)
        self.pushButton_Apply.setObjectName(u"pushButton_Apply")

        self.gridLayout.addWidget(self.pushButton_Apply, 3, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_2 = QLabel(setGradient)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 4)

        self.GradWidget = QWidget(setGradient)
        self.GradWidget.setObjectName(u"GradWidget")

        self.gridLayout.addWidget(self.GradWidget, 1, 0, 1, 4)

        self.pushButton_Save = QPushButton(setGradient)
        self.pushButton_Save.setObjectName(u"pushButton_Save")

        self.gridLayout.addWidget(self.pushButton_Save, 3, 3, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.pushButton_Reverse = QPushButton(setGradient)
        self.pushButton_Reverse.setObjectName(u"pushButton_Reverse")

        self.gridLayout.addWidget(self.pushButton_Reverse, 3, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.pushButton_Apply, self.pushButton_Reverse)
        QWidget.setTabOrder(self.pushButton_Reverse, self.pushButton_Load)
        QWidget.setTabOrder(self.pushButton_Load, self.pushButton_Save)

        self.retranslateUi(setGradient)

        QMetaObject.connectSlotsByName(setGradient)

    # setupUi

    def retranslateUi(self, setGradient):
        setGradient.setWindowTitle(QCoreApplication.translate("setGradient", u"Make a colourmap", None))
        self.label.setText(QCoreApplication.translate("setGradient", u"Make your own colourmap gradient:", None))
        self.pushButton_Load.setText(QCoreApplication.translate("setGradient", u"Load", None))
        self.pushButton_Apply.setText(QCoreApplication.translate("setGradient", u"Apply", None))
        self.label_2.setText(QCoreApplication.translate("setGradient", u"Left-click - create or move a point. \n"
                                                                       "Right-click - delete point. \n"
                                                                       "Double-click - change colour.", None))
        self.pushButton_Save.setText(QCoreApplication.translate("setGradient", u"Save", None))
        self.pushButton_Reverse.setText(QCoreApplication.translate("setGradient", u"Reverse", None))
    # retranslateUi
