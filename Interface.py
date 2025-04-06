import math
import sys

import matplotlib
import numpy as np
import json
from PySide6.QtCore import Slot, QSize, Qt, QTimer, QPointF
from PySide6.QtGui import QPalette, QIcon, QPixmap, QPainter, QColor, QBrush, QMouseEvent, QLinearGradient, QImage
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QMainWindow, QFileDialog, QMessageBox, QComboBox, \
    QColorDialog, QWidget
from matplotlib import colors
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

from Mandelbrot_Julia import mandelbrot_julia_set
from ui_form_MandelbrotJulia import Ui_MainWindowMandelbrotJulia
from ui_form_setGradient import Ui_setGradient
from ui_form_DialogSetLim import Ui_SetLimits
from ui_form_setShading import Ui_setShading
from ui_form_DialogSave import Ui_Save
from ui_form_setC import Ui_setC

matplotlib.use('Qt5Agg')

LIST_MANDELBROT_DICT = {'2': (-2, 0.5, -1.25, 1.25), '3': (-1, 1, -1.25, 1.25),
                        '4': (-1.35, 1, -1.25, 1.25), '5': (-1, 1, -1, 1),
                        '6': (-1.3, 1.2, -1.2, 1.2), '7': (-1.25, 1.25, -1.3, 1.3),
                        '8': (-1.25, 1.25, -1.3, 1.3)}


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)


class BaseDialog(QDialog):
    def __init__(self, ui_class, parent=None):
        super().__init__(parent)
        self.ui = ui_class()
        self.ui.setupUi(self)


class DialogSetLim(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(Ui_SetLimits, parent)
        self.setTabOrder(self.ui.lineEdit_X, self.ui.lineEdit_Y)
        self.setTabOrder(self.ui.lineEdit_Y, self.ui.lineEdit_XC)
        self.setTabOrder(self.ui.lineEdit_XC, self.ui.lineEdit_YC)
        self.setTabOrder(self.ui.lineEdit_YC, self.ui.lineEdit_deltaX)
        self.setTabOrder(self.ui.lineEdit_deltaX, self.ui.lineEdit_deltaY)


class DialogSave(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(Ui_Save, parent)
        self.setTabOrder(self.ui.lineEdit_L, self.ui.lineEdit_H)
        self.setTabOrder(self.ui.lineEdit_H, self.ui.lineEdit_DPI)


class DialogSetC(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(Ui_setC, parent)
        self.setTabOrder(self.ui.lineEdit_ReC, self.ui.lineEdit_ImC)
        self.setTabOrder(self.ui.lineEdit_ImC, self.ui.lineEdit_rhoC)
        self.setTabOrder(self.ui.lineEdit_rhoC, self.ui.lineEdit_phiC)


class DialogSetShading(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(Ui_setShading, parent)


class MyWindowMandelbrotJulia(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindowMandelbrotJulia()
        self.ui.setupUi(self)


class DialogSetGradient(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(Ui_setGradient, parent)
        self.GradWidget = Gradient()
        self.ui.gridLayout.removeWidget(self.ui.GradWidget)
        self.ui.gridLayout.addWidget(self.GradWidget, 1, 0, 1, 3)


class Gradient(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # [(position [0-1], QColor)]
        self.points = [(0.0, QColor(255, 0, 0)), (1.0, QColor(0, 0, 255))]  # red and blue
        self.loaded_colours = None
        self.dragging_index = None
        self.radius = 5

    def paintEvent(self, event):  # parent method, run by self.update()
        painter = QPainter(self)
        gradient = self.make_gradient()
        painter.fillRect(self.rect(), QBrush(gradient))

        # draw control points
        if self.points:
            for i, (pos, _) in enumerate(self.points):
                x = int(pos * self.width())
                y = self.height() // 2

                painter.setPen(Qt.gray)
                painter.drawLine(x, 0, x, self.height())

                painter.setBrush(Qt.white)
                painter.setPen(Qt.black)
                painter.drawEllipse(QPointF(x, y), self.radius, self.radius)

    def mousePressEvent(self, event: QMouseEvent):
        x = event.position().x()

        # right click - remove the point
        if event.button() == Qt.RightButton:
            for i, (pos, _) in enumerate(self.points):
                px = pos * self.width()
                if abs(px - x) <= self.radius:
                    if len(self.points) > 2:
                        del self.points[i]
                        self.update()
                    return

        # check if clicked on existing point
        for i, (pos, _) in enumerate(self.points):
            px = pos * self.width()
            if abs(px - x) <= self.radius:
                self.dragging_index = i
                return

        # otherwise, add a new point
        pos = x / self.width()
        colour = QColorDialog.getColor()
        self.activateWindow()
        self.raise_()
        if colour.isValid():
            self.points.append((pos, colour))
            self.points.sort()
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging_index is not None:
            x = event.position().x()
            pos = max(0.0, min(1.0, x / self.width()))  # check for out-of-bounds
            colour = self.points[self.dragging_index][1]
            self.points[self.dragging_index] = (pos, colour)
            self.points.sort()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.dragging_index = None

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        # on double click: change colour if clicked on a point
        x = event.position().x()
        for i, (pos, _) in enumerate(self.points):
            px = pos * self.width()
            if abs(px - x) <= self.radius:
                new_colour = QColorDialog.getColor()
                if new_colour.isValid():
                    self.points[i] = (pos, new_colour)
                    self.update()
                return

    def make_gradient(self):
        gradient = QLinearGradient(0, 0, self.width(), 0)
        if self.points:
            for pos, colour in sorted(self.points):
                gradient.setColorAt(pos, colour)
        elif self.loaded_colours:
            num_colours = len(self.loaded_colours)
            for i, colour in enumerate(self.loaded_colours):
                pos = i / (num_colours - 1)
                gradient.setColorAt(pos, QColor(*colour))
        return gradient

    def make_colourmap(self, steps=256):
        gradient = self.make_gradient()
        image = QImage(self.width(), self.height(), QImage.Format_RGB32)
        painter = QPainter(image)  # draw an image and then scan its colours
        painter.fillRect(image.rect(), gradient)
        painter.end()

        colours = []
        for i in range(steps):
            x = int(i / (steps - 1) * (self.width() - 1))
            colour = image.pixelColor(x, self.height() // 2)
            colours.append((colour.red() / 255.0, colour.green() / 255.0, colour.blue() / 255.0, 1.0))  # RGBA

        return colors.ListedColormap(colours)

    def save_to_file(self, path, steps=256):
        colourmap = self.make_colourmap(steps)

        colours_data = []
        for color in colourmap.colors:
            colours_data.append({'r': color[0], 'g': color[1], 'b': color[2]})

        with open(path, 'w') as f:
            json.dump(colours_data, fp=f, indent=2)

    def load_from_file(self, path):
        try:
            with open(path, 'r') as f:
                colours_data = json.load(f)

            colours = []
            for colour in colours_data:
                r = colour['r']
                g = colour['g']
                b = colour['b']
                colours.append((round(r*255), round(g*255), round(b*255)))

            self.points = []
            self.loaded_colours = colours
            self.update()

        except Exception as e:
            print('Cannot load the colourmap:', e)


class MJSet(MyWindowMandelbrotJulia):
    def __init__(self, application: QApplication = None, parent=None):
        super().__init__(parent)
        self.mode = 'mandelbrot'
        self.horizon = 2e50
        self.x_c_0 = -0.8000
        self.y_c_0 = -0.1560
        self.x_c = self.x_c_0
        self.y_c = self.y_c_0
        self.height = 1000
        self.length = 1000
        self.colourmap = 'jet'
        self.slider_move = False
        self.rebuild = False
        self.set_lim_dialog = None
        self.save_image_dialog = None
        self.power = 2
        self.set_c_dialog = None
        self.shading_dialog = None
        self.shading = False
        self.azdeg = None
        self.altdeg = None
        self.vert_exag = None
        self.application = application
        self.toolbar = None
        self.gradient_dialog = None

        self.ui.groupbox_C.setVisible(False)

        self.ui.comboBox_Set.addItems(['mandelbrot', 'julia'])
        self.ui.comboBox_Set.setCurrentText(self.mode)
        self.ui.comboBox_Set.activated.connect(self.mode_update)

        self.ui.comboBox_Power.addItems(['2', '3', '4', '5', '6', '7', '8'])
        self.ui.comboBox_Power.setCurrentText('2')

        self.sc = MplCanvas(self)
        self.ax = self.sc.ax
        self.fig = self.sc.fig
        self.fig.patch.set_facecolor(self.ui.centralwidget.palette().color(QPalette.Window).name())
        if self.application.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            self.ax.tick_params(axis='both', colors='w')
        self.application.styleHints().colorSchemeChanged.connect(
            lambda: QTimer.singleShot(100, self.colour_scheme_changed))
        self.ax.imshow([[0]], origin='lower', cmap=self.colourmap)  # Empty initial image
        self.ax.set(xlim=(self.xmin_0, self.xmax_0), ylim=(self.ymin_0, self.ymax_0))
        self.ax.callbacks.connect('ylim_changed', self.ax_update)
        self.ax.set(xlim=(self.xmin_0, self.xmax_0), ylim=(self.ymin_0, self.ymax_0))
        im = self.ax.images[0]
        im.set(clim=(im.get_array().min(), im.get_array().max()))
        self.fig.tight_layout()
        self.ui.lineEdit_N.setText(f'{self.n}')
        self.ui.lineEdit_H.setText(f'{self.horizon:.1e}')

        self.toolbar = NavigationToolbar(self.sc, self)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.sc)
        self.main_layout.addWidget(self.toolbar)
        self.ui.frame.setLayout(self.main_layout)

        self.ui.horizontalSlider_N.setValue(self.n)

        self.ui.horizontalSlider_N.valueChanged.connect(self.change_n)
        self.ui.pushButton_ResetN.clicked.connect(self.reset_n)

        delta_slider_c = 5e-4
        ini_slider_xc_val = (self.x_c_0 + 1) / delta_slider_c
        ini_slider_yc_val = (self.y_c_0 + 1) / delta_slider_c

        self.ui.horizontalSlider_XC.setValue(round(ini_slider_xc_val))
        self.ui.horizontalSlider_YC.setValue(round(ini_slider_yc_val))
        self.ui.horizontalSlider_XC.valueChanged.connect(lambda: self.set_xyc('x'))
        self.ui.horizontalSlider_YC.valueChanged.connect(lambda: self.set_xyc('y'))
        self.ui.pushButton_ResetC.clicked.connect(self.reset_c)

        self.ui.pushButton_setC.clicked.connect(self.set_c_dial)

        rho, phi = self.polar_coordinates(self.x_c, self.y_c)
        self.ui.label_C.setText(
            f'C = {self.x_c:.4f} {self.y_c:+.4f}\U0001D456 = {rho:.4f}\U000022C5exp({phi:.4f}\U0001D456)')

        for i, cmap in enumerate(plt.colormaps()):
            if i == 0:
                self.ui.comboBox_Colourmap.setIconSize(QPixmap(f'colour_pic/{cmap}.png').scaled(100, 20).size())
            pixmap = QPixmap(f'colour_pic/{cmap}.png').scaled(100, 20)
            icon = QIcon(pixmap)
            self.ui.comboBox_Colourmap.addItem(icon, cmap)
        self.ui.comboBox_Colourmap.addItem('Set your own colourmap...')
        self.ui.comboBox_Colourmap.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.ui.comboBox_Colourmap.setMinimumContentsLength(3)
        self.ui.comboBox_Colourmap.setCurrentText(self.colourmap)
        self.ui.comboBox_Colourmap.activated.connect(self.colourmap_update)
        self.ui.pushButton_setShading.clicked.connect(self.set_shading_dialog)
        self.ui.pushButton_removeShading.clicked.connect(self.remove_shading)

        self.ui.pushButton_Rebuild.clicked.connect(self.rebuild_im)
        self.ui.pushButton_Reset.clicked.connect(self.reset_im)

        self.ui.pushButton_zoom_plus.clicked.connect(lambda: self.zoom('plus'))
        self.ui.pushButton_zoom_minus.clicked.connect(lambda: self.zoom('minus'))
        self.ui.pushButton_NewLims.clicked.connect(self.set_limits_dialog)
        self.ui.pushButton_ResetLims.clicked.connect(self.reset_lims)

        self.ui.pushButton_Save.clicked.connect(self.save_image)

    def ax_update(self, event=None):
        n = self.n
        if self.horizon < 4:
            self.horizon = 4
            self.ui.lineEdit_H.setText('4')
        self.ax.set_autoscale_on(False)  # Otherwise, infinite loop
        im = self.ax.images[0]
        xmin, xmax, ymin, ymax = np.float64([*self.ax.get_xlim(), *self.ax.get_ylim()])
        print('lims =', xmin, xmax, ymin, ymax)
        self.ui.label_limX.setText(f'({xmin:.16f},\n {xmax:.16f})')
        self.ui.label_limY.setText(f'({ymin:.16f},\n {ymax:.16f})')
        self.ui.label_coordC.setText(f'({xmin + (xmax - xmin) / 2:.16f},\n {ymin + (ymax - ymin) / 2:.16f})')
        if self.mode == 'julia':
            print('x_c, y_c =', self.x_c, self.y_c)
        print('n, diff =', n, xmax - xmin, ymax - ymin)
        print(xmin, xmax, ymin, ymax, n, self.horizon, self.length, self.height)
        if not self.shading:
            im.set(data=mandelbrot_julia_set(xmin, xmax, ymin, ymax, horizon=self.horizon,
                                             length=self.length, height=self.height, n=n,
                                             x_c=self.x_c, y_c=self.y_c, power=self.power, mode=self.mode)[2].T,
                   extent=(xmin, xmax, ymin, ymax), cmap=self.colourmap)
        else:
            light = colors.LightSource(azdeg=self.azdeg, altdeg=self.altdeg)
            data = mandelbrot_julia_set(xmin, xmax, ymin, ymax, horizon=self.horizon,
                                        length=self.length, height=self.height, n=n,
                                        x_c=self.x_c, y_c=self.y_c, power=self.power, mode=self.mode)[2].T
            data = light.shade(data, cmap=plt.get_cmap(self.colourmap), vert_exag=self.vert_exag,
                               norm=colors.PowerNorm(0.3), blend_mode='hsv')
            im.set(data=data, extent=(xmin, xmax, ymin, ymax))
        print('min, max =', im.get_array().min(), im.get_array().max(), '\n')
        im.set(clim=(im.get_array().min(), im.get_array().max()))
        self.fig.canvas.draw_idle()
        self.fig.tight_layout()

    @property
    def xmin_0(self):
        if self.mode == 'mandelbrot':
            return LIST_MANDELBROT_DICT[str(self.power)][0]
        elif self.mode == 'julia':
            return -2.0

    @property
    def xmax_0(self):
        if self.mode == 'mandelbrot':
            return LIST_MANDELBROT_DICT[str(self.power)][1]
        elif self.mode == 'julia':
            return 2.0

    @property
    def ymin_0(self):
        if self.mode == 'mandelbrot':
            return LIST_MANDELBROT_DICT[str(self.power)][2]
        elif self.mode == 'julia':
            return -1.3

    @property
    def ymax_0(self):
        if self.mode == 'mandelbrot':
            return LIST_MANDELBROT_DICT[str(self.power)][3]
        elif self.mode == 'julia':
            return 1.3

    @property
    def n(self):
        if self.rebuild:
            nn = int(float(self.ui.lineEdit_N.text()))
            self.ui.lineEdit_N.setText(str(nn))
            return nn
        if self.slider_move:
            print('slider moved')
            return self.ui.horizontalSlider_N.value()
        else:
            xmin, xmax, ymin, ymax = np.float64([*self.ax.get_xlim(), *self.ax.get_ylim()])
            zoom = (self.xmax_0 - self.xmin_0) / (xmax - xmin)
            if zoom > 1:
                res = int(100 * (1 + math.log10(zoom)))
            else:
                res = 100
            self.ui.lineEdit_N.setText(f'{res}')
            # self.ui.horizontalSlider_N.setValue(res)
            # self.slider_move = False
            return res

    def reset_n(self):
        self.slider_move = False
        self.rebuild = False
        if self.n == self.ui.horizontalSlider_N.value():
            self.ax_update()
        else:
            self.ui.horizontalSlider_N.setValue(self.n)
            self.slider_move = False

    def change_n(self):
        self.slider_move = True
        self.rebuild = False
        self.ax_update()
        self.ui.lineEdit_N.setText(f'{self.n}')

    def set_xyc(self, regime):
        delta_slider_c = 5e-4
        if regime == 'x':
            i = self.ui.horizontalSlider_XC.value()
            self.x_c = -1 + delta_slider_c * i
        elif regime == 'y':
            i = self.ui.horizontalSlider_YC.value()
            self.y_c = -1 + delta_slider_c * i
        rho, phi = self.polar_coordinates(self.x_c, self.y_c)
        self.ui.label_C.setText(
            f'C = {self.x_c:.4f} {self.y_c:+.4f}\U0001D456 = {rho:.4f}\U000022C5exp({phi:.4f}\U0001D456)')
        self.ax_update()

    def polar_coordinates(self, x_c, y_c):
        rho = math.sqrt(x_c ** 2 + y_c ** 2)
        phi = math.atan2(y_c, x_c)
        phi = phi + 2 * math.pi * (phi < 0)
        return rho, phi

    def reset_c(self):
        delta_slider_c = 5e-4
        ini_slider_xc_val = (self.x_c_0 + 1) / delta_slider_c
        ini_slider_yc_val = (self.y_c_0 + 1) / delta_slider_c
        self.ui.horizontalSlider_XC.setValue(round(ini_slider_xc_val))
        self.ui.horizontalSlider_YC.setValue(round(ini_slider_yc_val))

    def set_c_dial(self):
        self.set_c_dialog = DialogSetC()
        self.set_c_dialog.ui.label_phiC.setText('Argument, \U000003D5:')
        self.set_c_dialog.ui.label_rhoC.setText('Modulus, \U000003C1:')
        self.set_c_dialog.ui.pushButton_RhoPhiC.setText('Set \U000003C1 and \U000003D5')
        self.set_c_dialog.ui.pushButto_ReImC.clicked.connect(lambda: self.set_c('imre'))
        self.set_c_dialog.ui.pushButton_RhoPhiC.clicked.connect(lambda: self.set_c('rhophi'))

        self.set_c_dialog.ui.lineEdit_ReC.setText(f'{self.x_c:.4f}')
        self.set_c_dialog.ui.lineEdit_ImC.setText(f'{self.y_c:.4f}')
        rho, phi = self.polar_coordinates(self.x_c, self.y_c)
        self.set_c_dialog.ui.lineEdit_rhoC.setText(f'{rho:.4f}')
        self.set_c_dialog.ui.lineEdit_phiC.setText(f'{phi:.4f}')

        self.set_c_dialog.exec()

    def set_c(self, regime):
        if regime == 'imre':
            self.x_c = float(self.set_c_dialog.ui.lineEdit_ReC.text())
            self.y_c = float(self.set_c_dialog.ui.lineEdit_ImC.text())
            rho, phi = self.polar_coordinates(self.x_c, self.y_c)
        elif regime == 'rhophi':
            rho = abs(float(self.set_c_dialog.ui.lineEdit_rhoC.text()))
            phi = float(self.set_c_dialog.ui.lineEdit_phiC.text()) % (2 * math.pi)
            self.x_c = rho * math.cos(phi)
            self.y_c = rho * math.sin(phi)
            phi = phi + 2 * math.pi * (phi < 0)
        self.ui.label_C.setText(
            f'C = {self.x_c:.4f} {self.y_c:+.4f}\U0001D456 = {rho:.4f}\U000022C5exp({phi:.4f}\U0001D456)')

        self.x_c = 1 if self.x_c > 1 else self.x_c
        self.y_c = 1 if self.y_c > 1 else self.y_c
        self.x_c = -1 if self.x_c < -1 else self.x_c
        self.y_c = -1 if self.y_c < -1 else self.y_c

        delta_slider_c = 5e-4
        slider_xc_val = (self.x_c + 1) / delta_slider_c
        slider_yc_val = (self.y_c + 1) / delta_slider_c

        self.ui.horizontalSlider_XC.setValue(round(slider_xc_val))
        self.ui.horizontalSlider_YC.setValue(round(slider_yc_val))
        self.set_c_dialog.accept()
        self.set_c_dialog.deleteLater()
        self.set_c_dialog = None

    @Slot()
    def colourmap_update(self):
        if self.ui.comboBox_Colourmap.currentIndex() == self.ui.comboBox_Colourmap.count() - 1:
            self.gradient_dialog = DialogSetGradient()
            self.gradient_dialog.ui.pushButton_Apply.clicked.connect(self.create_and_set_colourmap)
            self.gradient_dialog.ui.pushButton_Save.clicked.connect(self.save_colourmap)
            self.gradient_dialog.ui.pushButton_Load.clicked.connect(self.load_colourmap)
            self.gradient_dialog.show()
        else:
            self.colourmap = self.ui.comboBox_Colourmap.currentText()
            if not self.shading:
                im = self.ax.images[0]
                im.set(cmap=self.colourmap)
                self.fig.canvas.draw_idle()
            else:
                self.ax_update()

    def create_and_set_colourmap(self):
        self.colourmap = self.gradient_dialog.GradWidget.make_colourmap()
        if not self.shading:
            im = self.ax.images[0]
            im.set(cmap=self.colourmap)
            self.fig.canvas.draw_idle()
        else:
            self.ax_update()

    def save_colourmap(self):
        fname = QFileDialog.getSaveFileName(self, caption='Choose a filename to save to',
                                            dir='$HOME/Desktop/Colourmap.json',
                                            filter='json(*.json)')[0]
        self.gradient_dialog.activateWindow()
        self.gradient_dialog.raise_()

        if not fname:
            return

        self.gradient_dialog.GradWidget.save_to_file(fname)

    def load_colourmap(self):
        fname = QFileDialog.getOpenFileName(self, caption='Choose a filename to load from',
                                            filter='json(*.json)')[0]
        self.colourmap = self.gradient_dialog.GradWidget.load_from_file(fname)

    def colour_scheme_changed(self):
        self.fig.patch.set_facecolor(self.ui.centralwidget.palette().color(QPalette.Window).name())
        if self.application.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            self.ax.tick_params(axis='both', colors='w')
        else:
            self.ax.tick_params(axis='both', colors='k')
        self.fig.canvas.draw_idle()
        self.main_layout.removeWidget(self.toolbar)
        self.toolbar = NavigationToolbar(self.sc, self)
        self.main_layout.addWidget(self.toolbar)

    def set_shading_dialog(self):
        self.shading_dialog = DialogSetShading()
        if self.shading:
            self.shading_dialog.ui.lineEdit_azimuth.setText(str(self.azdeg))
            self.shading_dialog.ui.lineEdit_altitude.setText(str(self.altdeg))
            self.shading_dialog.ui.lineEdit_vert_exag.setText(str(self.vert_exag))
        else:
            self.shading_dialog.ui.lineEdit_azimuth.setText('315')
            self.shading_dialog.ui.lineEdit_altitude.setText('5')
            self.shading_dialog.ui.lineEdit_vert_exag.setText('1')
        self.shading_dialog.ui.pushButton_setShading.clicked.connect(self.set_shading)
        self.shading_dialog.exec()

    def set_shading(self):
        self.shading = True
        self.azdeg = float(self.shading_dialog.ui.lineEdit_azimuth.text())
        if self.azdeg < 0:
            self.azdeg = 0
        elif self.azdeg > 360:
            self.azdeg = 360
        self.altdeg = float(self.shading_dialog.ui.lineEdit_altitude.text())
        if self.altdeg < 0:
            self.altdeg = 0
        elif self.altdeg > 90:
            self.altdeg = 90
        self.vert_exag = float(self.shading_dialog.ui.lineEdit_vert_exag.text())
        self.ax_update()
        self.shading_dialog.accept()
        self.shading_dialog.deleteLater()
        self.shading_dialog = None

    def remove_shading(self):
        if not self.shading:
            pass
        else:
            self.shading = False
            self.ax_update()

    @Slot()
    def rebuild_im(self):
        self.power = int(self.ui.comboBox_Power.currentText())
        self.horizon = float(self.ui.lineEdit_H.text())
        self.rebuild = True
        self.ax_update()

    @Slot()
    def reset_im(self):
        if self.mode == 'mandelbrot':
            self.horizon = 2e50
        elif self.mode == 'julia':
            self.horizon = 4
        self.power = 2
        self.reset_n()
        self.ui.lineEdit_H.setText(f'{self.horizon:.1e}')
        self.ui.comboBox_Power.setCurrentText(str(self.power))

    @Slot()
    def mode_update(self):
        self.mode = self.ui.comboBox_Set.currentText()
        if self.mode == 'julia':
            self.ui.frame.setMinimumSize(QSize(630, 517))
            self.ui.groupbox_C.setVisible(True)
        elif self.mode == 'mandelbrot':
            self.ui.frame.setMinimumSize(QSize(630, 630))
            self.ui.groupbox_C.setVisible(False)
        if not self.isFullScreen():
            self.adjustSize()
        self.reset_lims()
        self.reset_im()

    @Slot()
    def reset_lims(self):
        self.ax.set_xlim(self.xmin_0, self.xmax_0)
        self.ax.set_ylim(self.ymin_0, self.ymax_0)

    @Slot()
    def set_limits_dialog(self):
        self.set_lim_dialog = DialogSetLim()
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        x_c = xmin + (xmax - xmin) / 2
        y_c = ymin + (ymax - ymin) / 2
        self.set_lim_dialog.ui.lineEdit_X.setText(f'{xmin:.16f}, {xmax:.16f}')
        self.set_lim_dialog.ui.lineEdit_Y.setText(f'{ymin:.16f}, {ymax:.16f}')
        self.set_lim_dialog.ui.lineEdit_XC.setText(f'{x_c:.16f}')
        self.set_lim_dialog.ui.lineEdit_YC.setText(f'{y_c:.16f}')
        self.set_lim_dialog.ui.lineEdit_deltaX.setText(f'{xmax - xmin:.16f}')
        self.set_lim_dialog.ui.lineEdit_deltaY.setText(f'{ymax - ymin:.16f}')

        self.set_lim_dialog.ui.pushButton_SetLim.clicked.connect(lambda: self.set_limits('xy'))
        self.set_lim_dialog.ui.pushButton_SetC.clicked.connect(lambda: self.set_limits('centre'))
        self.set_lim_dialog.exec()

    @Slot()
    def set_limits(self, regime):
        if regime == 'xy':
            lims = self.set_lim_dialog.ui.lineEdit_X.text().split(',')
            xmin, xmax = np.float64(lims)
            lims = self.set_lim_dialog.ui.lineEdit_Y.text().split(',')
            ymin, ymax = np.float64(lims)
        elif regime == 'centre':
            x_centre = np.float64(self.set_lim_dialog.ui.lineEdit_XC.text())
            y_centre = np.float64(self.set_lim_dialog.ui.lineEdit_YC.text())
            delta_x = np.float64(self.set_lim_dialog.ui.lineEdit_deltaX.text())
            delta_y = np.float64(self.set_lim_dialog.ui.lineEdit_deltaY.text())
            xmin = x_centre - delta_x / 2
            xmax = x_centre + delta_x / 2
            ymin = y_centre - delta_y / 2
            ymax = y_centre + delta_y / 2
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)
        self.set_lim_dialog.accept()
        self.set_lim_dialog.deleteLater()
        self.set_lim_dialog = None

    def zoom(self, regime):
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        if regime == 'plus':
            scale = 2.0
        elif regime == 'minus':
            scale = 0.5
        xmin_new = (xmin + xmax) / 2 - (xmax - xmin) / (2 * scale)
        xmax_new = (xmin + xmax) / 2 + (xmax - xmin) / (2 * scale)
        ymin_new = (ymin + ymax) / 2 - (ymax - ymin) / (2 * scale)
        ymax_new = (ymin + ymax) / 2 + (ymax - ymin) / (2 * scale)
        self.ax.set_xlim(xmin_new, xmax_new)
        self.ax.set_ylim(ymin_new, ymax_new)

    def save_image(self):
        self.save_image_dialog = DialogSave()
        self.save_image_dialog.ui.lineEdit_L.editingFinished.connect(lambda: self.edit_size('L'))
        self.save_image_dialog.ui.lineEdit_H.editingFinished.connect(lambda: self.edit_size('H'))
        self.save_image_dialog.ui.lineEdit_DPI.editingFinished.connect(self.edit_size_label)
        self.save_image_dialog.ui.checkBox_withAxes.stateChanged.connect(self.edit_size_label)
        self.save_image_dialog.ui.checkBox_lockAR.stateChanged.connect(lambda: self.edit_size('L'))

        self.save_image_dialog.ui.lineEdit_L.setText('10')
        self.save_image_dialog.ui.lineEdit_H.setText('10')
        self.save_image_dialog.ui.lineEdit_DPI.setText('300')

        self.save_image_dialog.ui.label_Size.setText('Image size: \n3000 \U000000D7 3000 pix.')

        self.save_image_dialog.ui.pushButton_Save.clicked.connect(self.save_dial)

        self.save_image_dialog.exec()

    def save_dial(self):
        filter_save = ('Portable Network Graphics (*.png);; Joint Photographic Expects Group (*jpeg *.jpg);; '
                       'Tagged Image File Format (*.tiff);; Portable Document Format (*.pdf);; '
                       'Encapsulated PostScript (*.eps)')
        fname = QFileDialog.getSaveFileName(self, caption='Choose a filename to save to',
                                            dir='$HOME/Desktop/Image.png',
                                            filter=filter_save)[0]
        if not fname:
            return

        self.save_file(fname)

    def save_file(self, filename):
        self.save_image_dialog.ui.pushButton_Save.setEnabled(False)
        length = int(self.save_image_dialog.ui.lineEdit_L.text())
        height = int(self.save_image_dialog.ui.lineEdit_H.text())
        dpi = int(self.save_image_dialog.ui.lineEdit_DPI.text())
        img_width = dpi * length
        img_height = dpi * height
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        print(xmin, xmax, ymin, ymax, self.x_c, self.y_c, self.horizon)
        x, y, z = mandelbrot_julia_set(xmin, xmax, ymin, ymax, self.x_c, self.y_c, img_height, img_width,
                                       self.n, self.horizon, power=self.power, mode=self.mode)
        if self.save_image_dialog.ui.checkBox_withAxes.isChecked():
            fig, ax = plt.subplots(figsize=(length, height), dpi=dpi)
            if not self.shading:
                ax.imshow(z.T, origin='lower', cmap=self.colourmap, extent=(xmin, xmax, ymin, ymax))
            else:
                light = colors.LightSource(azdeg=self.azdeg, altdeg=self.altdeg)
                data = light.shade(z.T, cmap=plt.get_cmap(self.colourmap), vert_exag=self.vert_exag,
                                   norm=colors.PowerNorm(0.3), blend_mode='hsv')
                ax.imshow(data, extent=(xmin, xmax, ymin, ymax), origin='lower')
            ax.tick_params(labelsize='xx-large')
            ax.xaxis.offsetText.set_fontsize('xx-large')
            ax.yaxis.offsetText.set_fontsize('xx-large')
            plt.tight_layout()
            plt.savefig(filename, dpi=dpi)
        else:
            if not self.shading:
                plt.imsave(filename, z.T, dpi=dpi, cmap=self.colourmap, origin='lower')
            else:
                light = colors.LightSource(azdeg=self.azdeg, altdeg=self.altdeg)
                data = light.shade(z.T, cmap=plt.get_cmap(self.colourmap), vert_exag=self.vert_exag,
                                   norm=colors.PowerNorm(0.3), blend_mode='hsv')
                plt.imsave(filename, data, dpi=dpi, origin='lower')
        QMessageBox.information(self, 'Save File', f'Image is saved to {filename}')
        self.save_image_dialog.ui.pushButton_Save.setEnabled(True)

    def edit_size_label(self):
        ll = int(self.save_image_dialog.ui.lineEdit_L.text())
        h = int(self.save_image_dialog.ui.lineEdit_H.text())
        dpi = int(self.save_image_dialog.ui.lineEdit_DPI.text())
        self.save_image_dialog.ui.label_Size.setText(f'Image size: \n{ll * dpi} \U000000D7 {h * dpi} pix.')

    def edit_size(self, regime):
        if self.save_image_dialog.ui.checkBox_lockAR.isChecked():
            aspect_ratio = np.diff(self.ax.get_ylim())[0] / np.diff(self.ax.get_xlim())[0]
            if regime == 'L':
                ll = int(self.save_image_dialog.ui.lineEdit_L.text())
                hh = round(ll * aspect_ratio)
                self.save_image_dialog.ui.lineEdit_H.setText(str(hh))
            elif regime == 'H':
                hh = int(self.save_image_dialog.ui.lineEdit_H.text())
                ll = round(hh / aspect_ratio)
                self.save_image_dialog.ui.lineEdit_L.setText(str(ll))
        self.edit_size_label()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MJSet(app)
    window.show()
    sys.exit(app.exec())
