# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_Save(object):
    def setupUi(self, Save):
        if not Save.objectName():
            Save.setObjectName(u"Save")
        Save.resize(265, 251)
        Save.setMinimumSize(QSize(244, 251))
        Save.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(Save)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_H = QLineEdit(Save)
        self.lineEdit_H.setObjectName(u"lineEdit_H")

        self.gridLayout.addWidget(self.lineEdit_H, 1, 1, 1, 1)

        self.label_DPI = QLabel(Save)
        self.label_DPI.setObjectName(u"label_DPI")

        self.gridLayout.addWidget(self.label_DPI, 2, 0, 1, 1)

        self.checkBox_withAxes = QCheckBox(Save)
        self.checkBox_withAxes.setObjectName(u"checkBox_withAxes")

        self.gridLayout.addWidget(self.checkBox_withAxes, 3, 0, 1, 1)

        self.label_L = QLabel(Save)
        self.label_L.setObjectName(u"label_L")

        self.gridLayout.addWidget(self.label_L, 0, 0, 1, 1)

        self.lineEdit_DPI = QLineEdit(Save)
        self.lineEdit_DPI.setObjectName(u"lineEdit_DPI")

        self.gridLayout.addWidget(self.lineEdit_DPI, 2, 1, 1, 1)

        self.label_Size = QLabel(Save)
        self.label_Size.setObjectName(u"label_Size")
        self.label_Size.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_Size, 4, 0, 1, 2)

        self.label_H = QLabel(Save)
        self.label_H.setObjectName(u"label_H")

        self.gridLayout.addWidget(self.label_H, 1, 0, 1, 1)

        self.pushButton_Save = QPushButton(Save)
        self.pushButton_Save.setObjectName(u"pushButton_Save")
        self.pushButton_Save.setAutoDefault(True)

        self.gridLayout.addWidget(self.pushButton_Save, 5, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)

        self.lineEdit_L = QLineEdit(Save)
        self.lineEdit_L.setObjectName(u"lineEdit_L")

        self.gridLayout.addWidget(self.lineEdit_L, 0, 1, 1, 1)

        self.checkBox_lockAR = QCheckBox(Save)
        self.checkBox_lockAR.setObjectName(u"checkBox_lockAR")

        self.gridLayout.addWidget(self.checkBox_lockAR, 3, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Save)

        QMetaObject.connectSlotsByName(Save)
    # setupUi

    def retranslateUi(self, Save):
        Save.setWindowTitle(QCoreApplication.translate("Save", u"Save Image", None))
        self.label_DPI.setText(QCoreApplication.translate("Save", u"DPI:", None))
        self.checkBox_withAxes.setText(QCoreApplication.translate("Save", u"With Axes", None))
        self.label_L.setText(QCoreApplication.translate("Save", u"Length:", None))
        self.label_Size.setText(QCoreApplication.translate("Save", u"The size of will be", None))
        self.label_H.setText(QCoreApplication.translate("Save", u"Height:", None))
        self.pushButton_Save.setText(QCoreApplication.translate("Save", u"Save", None))
        self.checkBox_lockAR.setText(QCoreApplication.translate("Save", u"Lock Aspect Ratio", None))
    # retranslateUi

