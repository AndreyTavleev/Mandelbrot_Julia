# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (QComboBox, QFrame, QGridLayout,
                               QGroupBox, QHBoxLayout, QLabel, QLayout,
                               QLineEdit, QPushButton, QScrollArea,
                               QSizePolicy, QSlider, QSpacerItem, QVBoxLayout,
                               QWidget)


class Ui_MainWindowMandelbrotJulia(object):
    def setupUi(self, MainWindowMandelbrotJulia):
        if not MainWindowMandelbrotJulia.objectName():
            MainWindowMandelbrotJulia.setObjectName(u"MainWindowMandelbrotJulia")
        MainWindowMandelbrotJulia.resize(900, 763)
        MainWindowMandelbrotJulia.setMinimumSize(QSize(900, 763))
        self.centralwidget = QWidget(MainWindowMandelbrotJulia)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
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
        self.frame.setMinimumSize(QSize(630, 517))
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

        self.label_C = QLabel(self.groupbox_C)
        self.label_C.setObjectName(u"label_C")
        font = QFont()
        font.setPointSize(15)
        self.label_C.setFont(font)
        self.label_C.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_C.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse | Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout_C.addWidget(self.label_C, 0, 0, 1, 2)

        self.comboBox_viewC = QComboBox(self.groupbox_C)
        self.comboBox_viewC.setObjectName(u"comboBox_viewC")

        self.gridLayout_C.addWidget(self.comboBox_viewC, 0, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addWidget(self.groupbox_C)

        self.horizontalLayout_Main.addLayout(self.verticalLayout)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy2)
        self.scrollArea.setMinimumSize(QSize(237, 0))
        self.scrollArea.setMaximumSize(QSize(230, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 236, 777))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_HNPColour = QVBoxLayout()
        self.verticalLayout_HNPColour.setObjectName(u"verticalLayout_HNPColour")
        self.verticalLayout_HNP = QVBoxLayout()
        self.verticalLayout_HNP.setObjectName(u"verticalLayout_HNP")
        self.gridLayout_HNP = QGridLayout()
        self.gridLayout_HNP.setObjectName(u"gridLayout_HNP")
        self.lineEdit_N = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_N.setObjectName(u"lineEdit_N")

        self.gridLayout_HNP.addWidget(self.lineEdit_N, 3, 1, 1, 1)

        self.label_Power = QLabel(self.scrollAreaWidgetContents)
        self.label_Power.setObjectName(u"label_Power")

        self.gridLayout_HNP.addWidget(self.label_Power, 1, 0, 1, 1)

        self.comboBox_Power = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_Power.setObjectName(u"comboBox_Power")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBox_Power.sizePolicy().hasHeightForWidth())
        self.comboBox_Power.setSizePolicy(sizePolicy3)
        self.comboBox_Power.setMinimumSize(QSize(50, 0))

        self.gridLayout_HNP.addWidget(self.comboBox_Power, 1, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.lineEdit_H = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_H.setObjectName(u"lineEdit_H")

        self.gridLayout_HNP.addWidget(self.lineEdit_H, 4, 1, 1, 1)

        self.label_N = QLabel(self.scrollAreaWidgetContents)
        self.label_N.setObjectName(u"label_N")

        self.gridLayout_HNP.addWidget(self.label_N, 3, 0, 1, 1)

        self.comboBox_Set = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_Set.setObjectName(u"comboBox_Set")

        self.gridLayout_HNP.addWidget(self.comboBox_Set, 0, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_HNP.addWidget(self.line_2, 2, 0, 1, 2)

        self.label_Set = QLabel(self.scrollAreaWidgetContents)
        self.label_Set.setObjectName(u"label_Set")

        self.gridLayout_HNP.addWidget(self.label_Set, 0, 0, 1, 1)

        self.label_Horizon = QLabel(self.scrollAreaWidgetContents)
        self.label_Horizon.setObjectName(u"label_Horizon")

        self.gridLayout_HNP.addWidget(self.label_Horizon, 4, 0, 1, 1)

        self.verticalLayout_HNP.addLayout(self.gridLayout_HNP)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_Rebuild = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_Rebuild.setObjectName(u"pushButton_Rebuild")

        self.horizontalLayout_3.addWidget(self.pushButton_Rebuild)

        self.pushButton_Reset = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_Reset.setObjectName(u"pushButton_Reset")

        self.horizontalLayout_3.addWidget(self.pushButton_Reset)

        self.verticalLayout_HNP.addLayout(self.horizontalLayout_3)

        self.verticalLayout_HNPColour.addLayout(self.verticalLayout_HNP)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_HNPColour.addWidget(self.line)

        self.label_Colourmap = QLabel(self.scrollAreaWidgetContents)
        self.label_Colourmap.setObjectName(u"label_Colourmap")
        self.label_Colourmap.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_HNPColour.addWidget(self.label_Colourmap)

        self.comboBox_Colourmap = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_Colourmap.setObjectName(u"comboBox_Colourmap")

        self.verticalLayout_HNPColour.addWidget(self.comboBox_Colourmap)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lineEdit_freq = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_freq.setObjectName(u"lineEdit_freq")
        self.lineEdit_freq.setMinimumSize(QSize(50, 0))

        self.gridLayout_3.addWidget(self.lineEdit_freq, 0, 3, 1, 1)

        self.label_freq = QLabel(self.scrollAreaWidgetContents)
        self.label_freq.setObjectName(u"label_freq")

        self.gridLayout_3.addWidget(self.label_freq, 0, 2, 1, 1)

        self.lineEdit_offset = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_offset.setObjectName(u"lineEdit_offset")

        self.gridLayout_3.addWidget(self.lineEdit_offset, 1, 3, 1, 1)

        self.label_offset = QLabel(self.scrollAreaWidgetContents)
        self.label_offset.setObjectName(u"label_offset")

        self.gridLayout_3.addWidget(self.label_offset, 1, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.comboBox_regime = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_regime.setObjectName(u"comboBox_regime")
        sizePolicy3.setHeightForWidth(self.comboBox_regime.sizePolicy().hasHeightForWidth())
        self.comboBox_regime.setSizePolicy(sizePolicy3)
        self.comboBox_regime.setMinimumSize(QSize(71, 0))

        self.gridLayout_3.addWidget(self.comboBox_regime, 0, 1, 2, 1)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 2, 1)

        self.verticalLayout_HNPColour.addLayout(self.gridLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_setShading = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_setShading.setObjectName(u"pushButton_setShading")

        self.horizontalLayout.addWidget(self.pushButton_setShading, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pushButton_removeShading = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_removeShading.setObjectName(u"pushButton_removeShading")

        self.horizontalLayout.addWidget(self.pushButton_removeShading, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_HNPColour.addLayout(self.horizontalLayout)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_HNPColour.addWidget(self.line_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.comboBox_SaveLoad = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_SaveLoad.setObjectName(u"comboBox_SaveLoad")

        self.horizontalLayout_4.addWidget(self.comboBox_SaveLoad)

        self.verticalLayout_HNPColour.addLayout(self.horizontalLayout_4)

        self.line_5 = QFrame(self.scrollAreaWidgetContents)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_HNPColour.addWidget(self.line_5)

        self.label_CurGrid = QLabel(self.scrollAreaWidgetContents)
        self.label_CurGrid.setObjectName(u"label_CurGrid")

        self.verticalLayout_HNPColour.addWidget(self.label_CurGrid, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_limX_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_limX_1.setObjectName(u"label_limX_1")

        self.verticalLayout_HNPColour.addWidget(self.label_limX_1, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_limX = QLabel(self.scrollAreaWidgetContents)
        self.label_limX.setObjectName(u"label_limX")
        self.label_limX.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse | Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_HNPColour.addWidget(self.label_limX, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_limY_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_limY_1.setObjectName(u"label_limY_1")

        self.verticalLayout_HNPColour.addWidget(self.label_limY_1, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_limY = QLabel(self.scrollAreaWidgetContents)
        self.label_limY.setObjectName(u"label_limY")
        self.label_limY.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse | Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_HNPColour.addWidget(self.label_limY, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_coordC_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_coordC_1.setObjectName(u"label_coordC_1")

        self.verticalLayout_HNPColour.addWidget(self.label_coordC_1, 0, Qt.AlignmentFlag.AlignHCenter)

        self.label_coordC = QLabel(self.scrollAreaWidgetContents)
        self.label_coordC.setObjectName(u"label_coordC")
        self.label_coordC.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse | Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_HNPColour.addWidget(self.label_coordC, 0, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalLayout_zoom = QHBoxLayout()
        self.horizontalLayout_zoom.setObjectName(u"horizontalLayout_zoom")
        self.pushButton_zoom_plus = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_zoom_plus.setObjectName(u"pushButton_zoom_plus")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ZoomIn))
        self.pushButton_zoom_plus.setIcon(icon)

        self.horizontalLayout_zoom.addWidget(self.pushButton_zoom_plus)

        self.pushButton_zoom_minus = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_zoom_minus.setObjectName(u"pushButton_zoom_minus")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ZoomOut))
        self.pushButton_zoom_minus.setIcon(icon1)

        self.horizontalLayout_zoom.addWidget(self.pushButton_zoom_minus)

        self.verticalLayout_HNPColour.addLayout(self.horizontalLayout_zoom)

        self.pushButton_NewLims = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_NewLims.setObjectName(u"pushButton_NewLims")

        self.verticalLayout_HNPColour.addWidget(self.pushButton_NewLims)

        self.pushButton_ResetLims = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_ResetLims.setObjectName(u"pushButton_ResetLims")

        self.verticalLayout_HNPColour.addWidget(self.pushButton_ResetLims)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_HNPColour.addItem(self.verticalSpacer_3)

        self.gridLayout.addLayout(self.verticalLayout_HNPColour, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_Main.addWidget(self.scrollArea)

        self.horizontalLayout_Main.setStretch(0, 1)

        self.gridLayout_2.addLayout(self.horizontalLayout_Main, 0, 0, 1, 1)

        MainWindowMandelbrotJulia.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.comboBox_Set, self.comboBox_Power)
        QWidget.setTabOrder(self.comboBox_Power, self.lineEdit_N)
        QWidget.setTabOrder(self.lineEdit_N, self.lineEdit_H)
        QWidget.setTabOrder(self.lineEdit_H, self.pushButton_Rebuild)
        QWidget.setTabOrder(self.pushButton_Rebuild, self.pushButton_Reset)
        QWidget.setTabOrder(self.pushButton_Reset, self.comboBox_Colourmap)
        QWidget.setTabOrder(self.comboBox_Colourmap, self.comboBox_regime)
        QWidget.setTabOrder(self.comboBox_regime, self.lineEdit_freq)
        QWidget.setTabOrder(self.lineEdit_freq, self.lineEdit_offset)
        QWidget.setTabOrder(self.lineEdit_offset, self.pushButton_setShading)
        QWidget.setTabOrder(self.pushButton_setShading, self.pushButton_removeShading)
        QWidget.setTabOrder(self.pushButton_removeShading, self.comboBox_SaveLoad)
        QWidget.setTabOrder(self.comboBox_SaveLoad, self.pushButton_zoom_plus)
        QWidget.setTabOrder(self.pushButton_zoom_plus, self.pushButton_zoom_minus)
        QWidget.setTabOrder(self.pushButton_zoom_minus, self.pushButton_NewLims)
        QWidget.setTabOrder(self.pushButton_NewLims, self.pushButton_ResetLims)
        QWidget.setTabOrder(self.pushButton_ResetLims, self.horizontalSlider_N)
        QWidget.setTabOrder(self.horizontalSlider_N, self.pushButton_ResetN)
        QWidget.setTabOrder(self.pushButton_ResetN, self.horizontalSlider_XC)
        QWidget.setTabOrder(self.horizontalSlider_XC, self.horizontalSlider_YC)
        QWidget.setTabOrder(self.horizontalSlider_YC, self.comboBox_viewC)
        QWidget.setTabOrder(self.comboBox_viewC, self.pushButton_setC)
        QWidget.setTabOrder(self.pushButton_setC, self.pushButton_ResetC)
        QWidget.setTabOrder(self.pushButton_ResetC, self.scrollArea)

        self.retranslateUi(MainWindowMandelbrotJulia)

        QMetaObject.connectSlotsByName(MainWindowMandelbrotJulia)

    # setupUi

    def retranslateUi(self, MainWindowMandelbrotJulia):
        MainWindowMandelbrotJulia.setWindowTitle(
            QCoreApplication.translate("MainWindowMandelbrotJulia", u"Mandelbrot & Julia Sets", None))
        self.pushButton_ResetN.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Reset N", None))
        self.label_XC.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"X_c:", None))
        self.pushButton_setC.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Set C", None))
        self.label_YC.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Y_c:", None))
        self.pushButton_ResetC.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Reset C", None))
        self.label_C.setText(
            QCoreApplication.translate("MainWindowMandelbrotJulia", u"C = x + i*y = rho * e^{i*phi}", None))
        self.label_Power.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Power:", None))
        self.label_N.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"N:", None))
        self.label_Set.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Set:", None))
        self.label_Horizon.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Horizon:", None))
        self.pushButton_Rebuild.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Rebuild", None))
        self.pushButton_Reset.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Reset", None))
        self.label_Colourmap.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Colourmap", None))
        self.label_freq.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"w:", None))
        self.label_offset.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"d:", None))
        self.label.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Regime:", None))
        self.pushButton_setShading.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Set \n"
                                                                                                   "shading", None))
        self.pushButton_removeShading.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Remove \n"
                                                                                                      "shading", None))
        self.label_2.setText(QCoreApplication.translate("MainWindowMandelbrotJulia", u"Save / Load:", None))
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
            QCoreApplication.translate("MainWindowMandelbrotJulia", u"Reset limits", None))
    # retranslateUi
