# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtWidgets import QCheckBox, QGridLayout, QLabel, QLineEdit, QPushButton, QWidget


class Ui_Save(object):
    def setupUi(self, Save):
        if not Save.objectName():
            Save.setObjectName(u"Save")
        Save.resize(263, 274)
        Save.setMinimumSize(QSize(263, 274))
        Save.setMaximumSize(QSize(263, 274))
        self.gridLayout_2 = QGridLayout(Save)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBox_withAxes = QCheckBox(Save)
        self.checkBox_withAxes.setObjectName(u"checkBox_withAxes")

        self.gridLayout.addWidget(self.checkBox_withAxes, 4, 0, 1, 1)

        self.label_DPI = QLabel(Save)
        self.label_DPI.setObjectName(u"label_DPI")

        self.gridLayout.addWidget(self.label_DPI, 2, 0, 1, 1)

        self.lineEdit_DPI = QLineEdit(Save)
        self.lineEdit_DPI.setObjectName(u"lineEdit_DPI")

        self.gridLayout.addWidget(self.lineEdit_DPI, 2, 1, 1, 1)

        self.label_Size = QLabel(Save)
        self.label_Size.setObjectName(u"label_Size")
        self.label_Size.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_Size, 5, 0, 1, 2)

        self.lineEdit_H = QLineEdit(Save)
        self.lineEdit_H.setObjectName(u"lineEdit_H")

        self.gridLayout.addWidget(self.lineEdit_H, 1, 1, 1, 1)

        self.label_H = QLabel(Save)
        self.label_H.setObjectName(u"label_H")

        self.gridLayout.addWidget(self.label_H, 1, 0, 1, 1)

        self.checkBox_lockAR = QCheckBox(Save)
        self.checkBox_lockAR.setObjectName(u"checkBox_lockAR")

        self.gridLayout.addWidget(self.checkBox_lockAR, 4, 1, 1, 1)

        self.pushButton_Save = QPushButton(Save)
        self.pushButton_Save.setObjectName(u"pushButton_Save")
        self.pushButton_Save.setAutoDefault(True)

        self.gridLayout.addWidget(self.pushButton_Save, 6, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)

        self.label_L = QLabel(Save)
        self.label_L.setObjectName(u"label_L")

        self.gridLayout.addWidget(self.label_L, 0, 0, 1, 1)

        self.lineEdit_L = QLineEdit(Save)
        self.lineEdit_L.setObjectName(u"lineEdit_L")

        self.gridLayout.addWidget(self.lineEdit_L, 0, 1, 1, 1)

        self.lineEdit_SS = QLineEdit(Save)
        self.lineEdit_SS.setObjectName(u"lineEdit_SS")

        self.gridLayout.addWidget(self.lineEdit_SS, 3, 1, 1, 1)

        self.label_SS = QLabel(Save)
        self.label_SS.setObjectName(u"label_SS")

        self.gridLayout.addWidget(self.label_SS, 3, 0, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_L, self.lineEdit_H)
        QWidget.setTabOrder(self.lineEdit_H, self.lineEdit_DPI)
        QWidget.setTabOrder(self.lineEdit_DPI, self.checkBox_withAxes)
        QWidget.setTabOrder(self.checkBox_withAxes, self.checkBox_lockAR)
        QWidget.setTabOrder(self.checkBox_lockAR, self.pushButton_Save)

        self.retranslateUi(Save)

        QMetaObject.connectSlotsByName(Save)

    # setupUi

    def retranslateUi(self, Save):
        Save.setWindowTitle(QCoreApplication.translate("Save", u"Save Image", None))
        self.checkBox_withAxes.setText(QCoreApplication.translate("Save", u"With Axes", None))
        self.label_DPI.setText(QCoreApplication.translate("Save", u"DPI:", None))
        self.label_Size.setText(QCoreApplication.translate("Save", u"The size of will be", None))
        self.label_H.setText(QCoreApplication.translate("Save", u"Height:", None))
        self.checkBox_lockAR.setText(QCoreApplication.translate("Save", u"Lock Aspect Ratio", None))
        self.pushButton_Save.setText(QCoreApplication.translate("Save", u"Save", None))
        self.label_L.setText(QCoreApplication.translate("Save", u"Length:", None))
        # if QT_CONFIG(tooltip)
        self.label_SS.setToolTip(QCoreApplication.translate("Save", u"SuperSampling Anti-Aliasing factor", None))
        # endif // QT_CONFIG(tooltip)
        self.label_SS.setText(QCoreApplication.translate("Save", u"SSAA:", None))
    # retranslateUi
