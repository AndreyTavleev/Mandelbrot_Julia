# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (QComboBox, QFrame, QGridLayout,
                               QGroupBox, QHBoxLayout, QLabel, QLayout,
                               QLineEdit, QPushButton, QSizePolicy,
                               QSlider, QSpacerItem, QVBoxLayout, QWidget)


class Ui_MainWindowMandelbrotJulia(object):
    def setupUi(self, MainWindowMandelbrotJulia):
        if not MainWindowMandelbrotJulia.objectName():
            MainWindowMandelbrotJulia.setObjectName(u"MainWindowMandelbrotJulia")
        MainWindowMandelbrotJulia.resize(844, 763)
        MainWindowMandelbrotJulia.setMinimumSize(QSize(844, 763))
        MainWindowMandelbrotJulia.setMaximumSize(QSize(16777215, 16777215))
        self.centralwidget = QWidget(MainWindowMandelbrotJulia)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_Main = QHBoxLayout()
        self.horizontalLayout_Main.setObjectName(u"horizontalLayout_Main")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(630, 630))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame)

        self.horizontalLayout_N = QHBoxLayout()
        self.horizontalLayout_N.setObjectName(u"horizontalLayout_N")
        self.horizontalSlider_N = QSlider(self.centralwidget)
        self.horizontalSlider_N.setObjectName(u"horizontalSlider_N")
        self.horizontalSlider_N.setMinimum(100)
        self.horizontalSlider_N.setMaximum(4000)
        self.horizontalSlider_N.setOrientation(Qt.Orientation.Horizontal)
        self.horizontalSlider_N.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.horizontalSlider_N.setTickInterval(200)

        self.horizontalLayout_N.addWidget(self.horizontalSlider_N, 0, Qt.AlignmentFlag.AlignVCenter)

        self.pushButton_ResetN = QPushButton(self.centralwidget)
        self.pushButton_ResetN.setObjectName(u"pushButton_ResetN")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_ResetN.sizePolicy().hasHeightForWidth())
        self.pushButton_ResetN.setSizePolicy(sizePolicy1)

        self.horizontalLayout_N.addWidget(self.pushButton_ResetN, 0,
                                          Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addLayout(self.horizontalLayout_N)

        self.groupbox_C = QGroupBox(self.centralwidget)
        self.groupbox_C.setObjectName(u"groupbox_C")
        self.gridLayout_C = QGridLayout(self.groupbox_C)
        self.gridLayout_C.setObjectName(u"gridLayout_C")
        self.label_C = QLabel(self.groupbox_C)
        self.label_C.setObjectName(u"label_C")
        font = QFont()
        font.setPointSize(15)
        self.label_C.setFont(font)
        self.label_C.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_C.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse | Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout_C.addWidget(self.label_C, 0, 0, 1, 3)

        self.label_XC = QLabel(self.groupbox_C)
        self.label_XC.setObjectName(u"label_XC")

        self.gridLayout_C.addWidget(self.label_XC, 1, 0, 1, 1)

        self.horizontalSlider_XC = QSlider(self.groupbox_C)
        self.horizontalSlider_XC.setObjectName(u"horizontalSlider_XC")
        self.horizontalSlider_XC.setMinimum(0)
        self.horizontalSlider_XC.setMaximum(4000)
        self.horizontalSlider_XC.setOrientation(Qt.Orientation.Horizontal)
        self.horizontalSlider_XC.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.horizontalSlider_XC.setTickInterval(200)

        self.gridLayout_C.addWidget(self.horizontalSlider_XC, 1, 1, 1, 1)

        self.pushButton_setC = QPushButton(self.groupbox_C)
        self.pushButton_setC.setObjectName(u"pushButton_setC")
        sizePolicy1.setHeightForWidth(self.pushButton_setC.sizePolicy().hasHeightForWidth())
        self.pushButton_setC.setSizePolicy(sizePolicy1)

        self.gridLayout_C.addWidget(self.pushButton_setC, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.label_YC = QLabel(self.groupbox_C)
        self.label_YC.setObjectName(u"label_YC")

        self.gridLayout_C.addWidget(self.label_YC, 2, 0, 1, 1)

        self.horizontalSlider_YC = QSlider(self.groupbox_C)
        self.horizontalSlider_YC.setObjectName(u"horizontalSlider_YC")
        self.horizontalSlider_YC.setMinimum(0)
        self.horizontalSlider_YC.setMaximum(4000)
        self.horizontalSlider_YC.setOrientation(Qt.Orientation.Horizontal)
        self.horizontalSlider_YC.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.horizontalSlider_YC.setTickInterval(200)

        self.gridLayout_C.addWidget(self.horizontalSlider_YC, 2, 1, 1, 1)

        self.pushButton_ResetC = QPushButton(self.groupbox_C)
        self.pushButton_ResetC.setObjectName(u"pushButton_ResetC")
        sizePolicy1.setHeightForWidth(self.pushButton_ResetC.sizePolicy().hasHeightForWidth())
        self.pushButton_ResetC.setSizePolicy(sizePolicy1)

        self.gridLayout_C.addWidget(self.pushButton_ResetC, 2, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addWidget(self.groupbox_C)

        self.horizontalLayout_Main.addLayout(self.verticalLayout)

        self.verticalLayout_HNPColour = QVBoxLayout()
        self.verticalLayout_HNPColour.setObjectName(u"verticalLayout_HNPColour")
        self.gridLayout_HNP = QGridLayout()
        self.gridLayout_HNP.setObjectName(u"gridLayout_HNP")
        self.label_Set = QLabel(self.centralwidget)
        self.label_Set.setObjectName(u"label_Set")

        self.gridLayout_HNP.addWidget(self.label_Set, 0, 0, 1, 1)

        self.lineEdit_H = QLineEdit(self.centralwidget)
        self.lineEdit_H.setObjectName(u"lineEdit_H")

        self.gridLayout_HNP.addWidget(self.lineEdit_H, 3, 1, 1, 1)

        self.comboBox_Set = QComboBox(self.centralwidget)
        self.comboBox_Set.setObjectName(u"comboBox_Set")

        self.gridLayout_HNP.addWidget(self.comboBox_Set, 0, 1, 1, 1)

        self.label_Power = QLabel(self.centralwidget)
        self.label_Power.setObjectName(u"label_Power")

        self.gridLayout_HNP.addWidget(self.label_Power, 5, 0, 1, 1)

        self.label_Horizon = QLabel(self.centralwidget)
        self.label_Horizon.setObjectName(u"label_Horizon")

        self.gridLayout_HNP.addWidget(self.label_Horizon, 3, 0, 1, 1)

        self.label_N = QLabel(self.centralwidget)
        self.label_N.setObjectName(u"label_N")

        self.gridLayout_HNP.addWidget(self.label_N, 4, 0, 1, 1)

        self.line_6 = QFrame(self.centralwidget)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_HNP.addWidget(self.line_6, 2, 0, 1, 2)

        self.lineEdit_N = QLineEdit(self.centralwidget)
        self.lineEdit_N.setObjectName(u"lineEdit_N")

        self.gridLayout_HNP.addWidget(self.lineEdit_N, 4, 1, 1, 1)

        self.comboBox_Power = QComboBox(self.centralwidget)
        self.comboBox_Power.setObjectName(u"comboBox_Power")

        self.gridLayout_HNP.addWidget(self.comboBox_Power, 5, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 19, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_HNP.addItem(self.verticalSpacer, 1, 0, 1, 2)

        self.verticalLayout_HNPColour.addLayout(self.gridLayout_HNP)

        self.pushButton_Rebuild = QPushButton(self.centralwidget)
        self.pushButton_Rebuild.setObjectName(u"pushButton_Rebuild")

        self.verticalLayout_HNPColour.addWidget(self.pushButton_Rebuild)

        self.pushButton_Reset = QPushButton(self.centralwidget)
        self.pushButton_Reset.setObjectName(u"pushButton_Reset")

        self.verticalLayout_HNPColour.addWidget(self.pushButton_Reset)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_HNPColour.addWidget(self.line)

        self.label_Colourmap = QLabel(self.centralwidget)
        self.label_Colourmap.setObjectName(u"label_Colourmap")
        self.label_Colourmap.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_HNPColour.addWidget(self.label_Colourmap)

        self.comboBox_Colourmap = QComboBox(self.centralwidget)
        self.comboBox_Colourmap.setObjectName(u"comboBox_Colourmap")

        self.verticalLayout_HNPColour.addWidget(self.comboBox_Colourmap)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_setShading = QPushButton(self.centralwidget)
        self.pushButton_setShading.setObjectName(u"pushButton_setShading")

        self.horizontalLayout.addWidget(self.pushButton_setShading, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pushButton_removeShading = QPushButton(self.centralwidget)
        self.pushButton_removeShading.setObjectName(u"pushButton_removeShading")

        self.horizontalLayout.addWidget(self.pushButton_removeShading, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_HNPColour.addLayout(self.horizontalLayout)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_HNPColour.addWidget(self.line_4)

        self.pushButton_Save = QPushButton(self.centralwidget)
        self.pushButton_Save.setObjectName(u"pushButton_Save")

        self.verticalLayout_HNPColour.addWidget(self.pushButton_Save)

        self.line_5 = QFrame(self.centralwidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_HNPColour.addWidget(self.line_5)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_HNPColour.addItem(self.verticalSpacer_2)

        self.label_CurGrid = QLabel(self.centralwidget)
        self.label_CurGrid.setObjectName(u"label_CurGrid")

        self.verticalLayout_HNPColour.addWidget(self.label_CurGrid, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_limX_1 = QLabel(self.centralwidget)
        self.label_limX_1.setObjectName(u"label_limX_1")

        self.verticalLayout_HNPColour.addWidget(self.label_limX_1, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_limX = QLabel(self.centralwidget)
        self.label_limX.setObjectName(u"label_limX")
        self.label_limX.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse | Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_HNPColour.addWidget(self.label_limX, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_limY_1 = QLabel(self.centralwidget)
        self.label_limY_1.setObjectName(u"label_limY_1")

        self.verticalLayout_HNPColour.addWidget(self.label_limY_1, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_limY = QLabel(self.centralwidget)
        self.label_limY.setObjectName(u"label_limY")
        self.label_limY.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse | Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_HNPColour.addWidget(self.label_limY, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_coordC_1 = QLabel(self.centralwidget)
        self.label_coordC_1.setObjectName(u"label_coordC_1")

        self.verticalLayout_HNPColour.addWidget(self.label_coordC_1, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_coordC = QLabel(self.centralwidget)
        self.label_coordC.setObjectName(u"label_coordC")
        self.label_coordC.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse | Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_HNPColour.addWidget(self.label_coordC, 0, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalLayout_zoom = QHBoxLayout()
        self.horizontalLayout_zoom.setObjectName(u"horizontalLayout_zoom")
        self.pushButton_zoom_plus = QPushButton(self.centralwidget)
        self.pushButton_zoom_plus.setObjectName(u"pushButton_zoom_plus")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ZoomIn))
        self.pushButton_zoom_plus.setIcon(icon)

        self.horizontalLayout_zoom.addWidget(self.pushButton_zoom_plus)

        self.pushButton_zoom_minus = QPushButton(self.centralwidget)
        self.pushButton_zoom_minus.setObjectName(u"pushButton_zoom_minus")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ZoomOut))
        self.pushButton_zoom_minus.setIcon(icon1)

        self.horizontalLayout_zoom.addWidget(self.pushButton_zoom_minus)

        self.verticalLayout_HNPColour.addLayout(self.horizontalLayout_zoom)

        self.pushButton_NewLims = QPushButton(self.centralwidget)
        self.pushButton_NewLims.setObjectName(u"pushButton_NewLims")

        self.verticalLayout_HNPColour.addWidget(self.pushButton_NewLims)

        self.pushButton_ResetLims = QPushButton(self.centralwidget)
        self.pushButton_ResetLims.setObjectName(u"pushButton_ResetLims")

        self.verticalLayout_HNPColour.addWidget(self.pushButton_ResetLims)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_HNPColour.addItem(self.verticalSpacer_3)

        self.horizontalLayout_Main.addLayout(self.verticalLayout_HNPColour)

        self.horizontalLayout_Main.setStretch(0, 1)

        self.gridLayout.addLayout(self.horizontalLayout_Main, 0, 0, 1, 1)

        MainWindowMandelbrotJulia.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindowMandelbrotJulia)

        QMetaObject.connectSlotsByName(MainWindowMandelbrotJulia)

    # setupUi

    def retranslateUi(self, MainWindowMandelbrotJulia):
        MainWindowMandelbrotJulia.setWindowTitle(
            QCoreApplication.translate("MainWindowMandelbrotJulia", u"Mandelbrot & Julia Sets", None))
        self.pushButton_ResetN.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Reset N", None))
        self.label_C.setText(
            QCoreApplication.translate("MainWindowMandelbrotJulia", u"C = x + i*y = rho * e^{i*phi}", None))
        self.label_XC.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"X_c:", None))
        self.pushButton_setC.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Set C", None))
        self.label_YC.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Y_c:", None))
        self.pushButton_ResetC.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Reset C", None))
        self.label_Set.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Set:", None))
        self.label_Power.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Power:", None))
        self.label_Horizon.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Horizon:", None))
        self.label_N.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"N:", None))
        self.pushButton_Rebuild.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Rebuild", None))
        self.pushButton_Reset.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Reset", None))
        self.label_Colourmap.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Colourmap", None))
        self.pushButton_setShading.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Set \n"
                                                                                                   "shading", None))
        self.pushButton_removeShading.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Remove \n"
                                                                                                      "shading", None))
        self.pushButton_Save.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Save", None))
        self.label_CurGrid.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Current grid:", None))
        self.label_limX_1.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"X-axis limits:", None))
        self.label_limX.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"TextLabel", None))
        self.label_limY_1.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Y-axis limits:", None))
        self.label_limY.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"TextLabel", None))
        self.label_coordC_1.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Centre:", None))
        self.label_coordC.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"TextLabel", None))
        self.pushButton_zoom_plus.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Zoom", None))
        self.pushButton_zoom_minus.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Zoom", None))
        self.pushButton_NewLims.setText(
            QCoreApplication.translate("MainWindowMandelbrotJulia", u"Set new limits", None))
        self.pushButton_ResetLims.setText(
            QCoreApplication.translate("MainWindowMandelbrotJulia", u"Reset Limits", None))
    # retranslateUi
