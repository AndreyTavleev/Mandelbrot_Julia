import math

import numpy as np
from PySide6.QtCore import QSize
from matplotlib import colors
from matplotlib import pyplot as plt

from fractal_calculation import mandelbrot_julia_set
from config import *
from ui_form_setLimits import Ui_setLimits
from ui_form_setC import Ui_setC


def cartesian_coordinates(rho_c, phi_c):
    x_c = rho_c * math.cos(phi_c)
    y_c = rho_c * math.sin(phi_c)
    return x_c, y_c


def polar_coordinates(x_c, y_c):
    rho = math.sqrt(x_c ** 2 + y_c ** 2)
    phi = math.atan2(y_c, x_c)
    phi = phi + 2 * math.pi * (phi < 0)  # Ensure the angle is in [0, 2pi]
    return rho, phi


class DialogSetC(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(Ui_setC, parent)


class DialogSetLimits(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(Ui_setLimits, parent)


class FractalControls:
    def ax_update(self, event=None):
        """
        Updates the axes of the plot with the current rendering parameters. Ensures proper
        limits, updates UI, and renders either Mandelbrot or Julia sets based on the
        selected mode and current settings.
        """
        n = self.n
        if self.horizon < 4:
            self.horizon = 4
            self.ui.lineEdit_H.setText('4')
        self.ax.set_autoscale_on(False)  # Otherwise, infinite loop
        im = self.ax.images[0]
        xmin, xmax, ymin, ymax = np.float64([*self.ax.get_xlim(), *self.ax.get_ylim()])
        print('lims =', xmin, xmax, ymin, ymax)
        # Update limits in GUI
        self.ui.label_limX.setText(f'({xmin:.16f},\n {xmax:.16f})')
        self.ui.label_limY.setText(f'({ymin:.16f},\n {ymax:.16f})')
        self.ui.label_coordC.setText(f'({xmin + (xmax - xmin) / 2:.16f},\n {ymin + (ymax - ymin) / 2:.16f})')
        if self.mode == 'julia':
            print('x_c, y_c =', self.x_c, self.y_c)
        print('n, diff =', n, xmax - xmin, ymax - ymin)
        print(xmin, xmax, ymin, ymax, n, self.horizon, self.length, self.height)
        data = mandelbrot_julia_set(xmin, xmax, ymin, ymax, horizon=self.horizon,
                                    length=self.length, height=self.height, n=n,
                                    x_c=self.x_c, y_c=self.y_c, power=self.power, mode=self.mode)[2].T
        if self.regime == 'sin':
            self.cache = data
            data = (np.sin(data * self.freq + self.offset)) ** 2
        if not self.shading:
            im.set(data=data, extent=(xmin, xmax, ymin, ymax), cmap=self.colourmap)
        else:
            light = colors.LightSource(azdeg=self.azdeg, altdeg=self.altdeg)
            data = light.shade(data, cmap=plt.get_cmap(self.colourmap), vert_exag=self.vert_exag,
                               blend_mode='hsv')
            im.set(data=data, extent=(xmin, xmax, ymin, ymax))
        im.set(clim=(im.get_array().min(), im.get_array().max()))
        self.fig.canvas.draw_idle()  # better than draw()
        self.fig.tight_layout()

    @property
    def n(self):
        if self.rebuild:
            nn = abs(int(float(self.ui.lineEdit_N.text())))
            self.ui.lineEdit_N.setText(str(nn))
            return nn
        if self.slider_move:
            return self.ui.horizontalSlider_N.value()
        else:
            xmin, xmax, ymin, ymax = np.float64([*self.ax.get_xlim(), *self.ax.get_ylim()])
            zoom = (self.xmax_0 - self.xmin_0) / (xmax - xmin)
            if zoom > 1:
                res = int(100 * (1 + math.log10(zoom)))
            else:
                res = 100
            self.ui.lineEdit_N.setText(f'{res}')
            self.no_ax_update = True
            self.ui.horizontalSlider_N.setValue(res)
            self.slider_move = False
            self.no_ax_update = False
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
        if not self.no_ax_update:
            self.ax_update()
        self.ui.lineEdit_N.setText(f'{self.n}')

    def set_power(self):
        old_power = self.power
        self.power = int(self.ui.comboBox_Power.currentText())
        if self.power == old_power:
            return
        if not self.no_ax_update:
            self.ax_update()


class JuliaParameterControl:
    def set_c_from_slider(self):
        if self.c_view == 'xy':
            i = self.ui.horizontalSlider_XC.value()
            self.x_c = -1 + self.delta_slider_xc * i
            i = self.ui.horizontalSlider_YC.value()
            self.y_c = -1 + self.delta_slider_yc * i
            self.rho_c, self.phi_c = polar_coordinates(self.x_c, self.y_c)
        elif self.c_view == 'rhophi':
            i = self.ui.horizontalSlider_XC.value()
            self.rho_c = self.delta_slider_xc * i
            i = self.ui.horizontalSlider_YC.value()
            self.phi_c = self.delta_slider_yc * i
            self.x_c, self.y_c = cartesian_coordinates(self.rho_c, self.phi_c)
        else:
            raise ValueError('Invalid c_view.')
        self.ui.label_C.setText(
            f'C = {self.x_c:.4f} {self.y_c:+.4f}\U0001D456 = '
            f'{self.rho_c:.4f}\U000022C5exp({self.phi_c:.4f}\U0001D456)')
        if not self.no_ax_update:
            self.ax_update()

    def change_c_view(self):
        c_view_old = self.c_view
        text = self.ui.comboBox_viewC.currentText()
        if text == 'ReC, ImC':
            self.c_view = 'xy'
            self.delta_slider_xc = DEFAULT_DELTA_SLIDER_C
            self.delta_slider_yc = DEFAULT_DELTA_SLIDER_C
        elif text == '\U000003C1, \U000003D5':
            self.c_view = 'rhophi'
            self.delta_slider_yc = (2.0 * np.pi) / 4000.0
            self.delta_slider_xc = math.sqrt(2) / 4000.0
        if c_view_old == self.c_view:
            return
        if self.c_view == 'xy':
            self.ui.label_XC.setText('X_c')
            self.ui.label_YC.setText('Y_c')
            self.x_c, self.y_c = cartesian_coordinates(self.rho_c, self.phi_c)
            slider_xc_val = self.from_value_to_slider(self.x_c, 'xc')
            slider_yc_val = self.from_value_to_slider(self.y_c, 'yc')
        elif self.c_view == 'rhophi':
            self.ui.label_XC.setText('\U000003C1')
            self.ui.label_YC.setText('\U000003D5')
            self.rho_c, self.phi_c = polar_coordinates(self.x_c, self.y_c)
            slider_xc_val = self.from_value_to_slider(self.rho_c, 'rho')
            slider_yc_val = self.from_value_to_slider(self.phi_c, 'phi')
        else:
            raise ValueError('Invalid c_view.')
        self.no_ax_update = True
        self.ui.horizontalSlider_XC.setValue(round(slider_xc_val))
        self.ui.horizontalSlider_YC.setValue(round(slider_yc_val))
        self.no_ax_update = False

    def from_value_to_slider(self, value, regime):
        if regime == 'xc':
            return (value + 1) / self.delta_slider_xc
        elif regime == 'yc':
            return (value + 1) / self.delta_slider_yc
        elif regime == 'rho':
            return value / self.delta_slider_xc
        elif regime == 'phi':
            return value / self.delta_slider_yc
        else:
            raise ValueError('Invalid regime.')

    def reset_c(self):
        if self.c_view == 'xy':
            ini_slider_xc_val = self.from_value_to_slider(self.x_c_0, 'xc')
            ini_slider_yc_val = self.from_value_to_slider(self.y_c_0, 'yc')
        elif self.c_view == 'rhophi':
            ini_slider_xc_val = self.from_value_to_slider(self.rho_c_0, 'rho')
            ini_slider_yc_val = self.from_value_to_slider(self.phi_c_0, 'phi')
        else:
            raise ValueError('Invalid c_view.')
        self.ui.horizontalSlider_XC.setValue(round(ini_slider_xc_val))
        self.ui.horizontalSlider_YC.setValue(round(ini_slider_yc_val))

    def show_set_c_dialog(self):
        self.set_c_dialog = DialogSetC()
        self.set_c_dialog.ui.label_phiC.setText('Argument, \U000003D5:')
        self.set_c_dialog.ui.label_rhoC.setText('Modulus, \U000003C1:')
        self.set_c_dialog.ui.pushButton_RhoPhiC.setText('Set \U000003C1 and \U000003D5')
        self.set_c_dialog.ui.pushButto_ReImC.clicked.connect(lambda: self.set_c('xy'))
        self.set_c_dialog.ui.pushButton_RhoPhiC.clicked.connect(lambda: self.set_c('rhophi'))

        self.set_c_dialog.ui.lineEdit_ReC.setText(f'{self.x_c:.4f}')
        self.set_c_dialog.ui.lineEdit_ImC.setText(f'{self.y_c:.4f}')
        self.set_c_dialog.ui.lineEdit_rhoC.setText(f'{self.rho_c:.4f}')
        self.set_c_dialog.ui.lineEdit_phiC.setText(f'{self.phi_c:.4f}')

        self.set_c_dialog.exec()

    def set_c(self, regime):
        if regime == 'xy':
            self.x_c = float(self.set_c_dialog.ui.lineEdit_ReC.text())
            self.y_c = float(self.set_c_dialog.ui.lineEdit_ImC.text())
            # Clamp values to (-1, 1)
            self.x_c = max(-1.0, min(1.0, self.x_c))
            self.y_c = max(-1.0, min(1.0, self.y_c))
            self.rho_c, self.phi_c = polar_coordinates(self.x_c, self.y_c)
        elif regime == 'rhophi':
            self.rho_c = abs(float(self.set_c_dialog.ui.lineEdit_rhoC.text()))
            # Clamp value to (0, sqrt(2))
            self.rho_c = max(0.0, min(math.sqrt(2.0), self.rho_c))
            self.phi_c = float(self.set_c_dialog.ui.lineEdit_phiC.text()) % (2 * math.pi)
            self.phi_c = self.phi_c + 2 * math.pi * (self.phi_c < 0)  # Ensure the angle is in [0, 2pi]
            self.x_c, self.y_c = cartesian_coordinates(self.rho_c, self.phi_c)
        else:
            raise ValueError('Invalid regime.')

        if self.c_view == 'xy':
            slider_xc_val = self.from_value_to_slider(self.x_c, 'xc')
            slider_yc_val = self.from_value_to_slider(self.y_c, 'yc')
        elif self.c_view == 'rhophi':
            slider_xc_val = self.from_value_to_slider(self.rho_c, 'rho')
            slider_yc_val = self.from_value_to_slider(self.phi_c, 'phi')
        else:
            raise ValueError('Invalid c_view.')

        self.ui.horizontalSlider_XC.setValue(round(slider_xc_val))
        self.ui.horizontalSlider_YC.setValue(round(slider_yc_val))
        self.set_c_dialog.accept()
        self.set_c_dialog.deleteLater()
        self.set_c_dialog = None


class ImageRenderer:
    def rebuild_im(self):
        self.horizon = float(self.ui.lineEdit_H.text())
        self.rebuild = True
        nn = self.n
        nn = nn * (nn != 0) or 1
        if 4000 >= nn >= 100:
            if nn == self.ui.horizontalSlider_N.value():
                if not self.no_ax_update:
                    self.ax_update()
            else:
                self.ui.horizontalSlider_N.setValue(nn)
                self.slider_move = False
                self.rebuild = True
        else:
            if self.no_ax_update:
                if nn >= 4000:
                    self.ui.horizontalSlider_N.setValue(4000)
                else:
                    self.ui.horizontalSlider_N.setValue(100)
                self.ui.lineEdit_N.setText(str(nn))
                self.slider_move = False
                self.rebuild = True
            else:
                self.no_ax_update = True
                if nn >= 4000:
                    self.ui.horizontalSlider_N.setValue(4000)
                else:
                    self.ui.horizontalSlider_N.setValue(100)
                self.no_ax_update = False
                self.ui.lineEdit_N.setText(str(nn))
                self.slider_move = False
                self.rebuild = True
                self.ax_update()

    def reset_im(self):
        if self.mode == 'mandelbrot':
            self.horizon = DEFAULT_HORIZON_MANDELBROT
        elif self.mode == 'julia':
            self.horizon = DEFAULT_HORIZON_JULIA
        self.reset_n()
        self.ui.lineEdit_H.setText(f'{self.horizon:.1e}')

    def mode_update(self):
        mode_old = self.mode
        self.mode = self.ui.comboBox_Set.currentText()
        if self.mode == mode_old:
            return
        if self.mode == 'julia':
            self.ui.frame.setMinimumSize(QSize(630, 517))
            self.ui.groupbox_C.setVisible(True)
        elif self.mode == 'mandelbrot':
            self.ui.frame.setMinimumSize(QSize(630, 630))
            self.ui.groupbox_C.setVisible(False)
        if not self.isFullScreen():
            self.adjustSize()
        self.power = DEFAULT_POWER
        self.ui.comboBox_Power.setCurrentText(str(self.power))
        if not self.no_ax_update:
            self.reset_lims()
            self.reset_im()


class CoordinateManager:
    @property
    def xmin_0(self):
        if self.mode == 'mandelbrot':
            return LIMS_MANDELBROT_DICT[str(self.power)][0]
        elif self.mode == 'julia':
            return -2.0

    @property
    def xmax_0(self):
        if self.mode == 'mandelbrot':
            return LIMS_MANDELBROT_DICT[str(self.power)][1]
        elif self.mode == 'julia':
            return 2.0

    @property
    def ymin_0(self):
        if self.mode == 'mandelbrot':
            return LIMS_MANDELBROT_DICT[str(self.power)][2]
        elif self.mode == 'julia':
            return -1.3

    @property
    def ymax_0(self):
        if self.mode == 'mandelbrot':
            return LIMS_MANDELBROT_DICT[str(self.power)][3]
        elif self.mode == 'julia':
            return 1.3

    def zoom(self, regime):
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        if regime == 'plus':
            scale = 2.0
        elif regime == 'minus':
            scale = 0.5
        else:
            raise ValueError('Invalid regime.')
        xmin_new = (xmin + xmax) / 2 - (xmax - xmin) / (2 * scale)
        xmax_new = (xmin + xmax) / 2 + (xmax - xmin) / (2 * scale)
        ymin_new = (ymin + ymax) / 2 - (ymax - ymin) / (2 * scale)
        ymax_new = (ymin + ymax) / 2 + (ymax - ymin) / (2 * scale)
        self.ax.set_xlim(xmin_new, xmax_new)
        self.ax.set_ylim(ymin_new, ymax_new)

    def reset_lims(self):
        self.ax.set_xlim(self.xmin_0, self.xmax_0)
        self.ax.set_ylim(self.ymin_0, self.ymax_0)

    def show_set_limits_dialog(self):
        self.set_limits_dialog = DialogSetLimits()
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        x_c = xmin + (xmax - xmin) / 2
        y_c = ymin + (ymax - ymin) / 2
        self.set_limits_dialog.ui.lineEdit_X.setText(f'{xmin:.16f}, {xmax:.16f}')
        self.set_limits_dialog.ui.lineEdit_Y.setText(f'{ymin:.16f}, {ymax:.16f}')
        self.set_limits_dialog.ui.lineEdit_XC.setText(f'{x_c:.16f}')
        self.set_limits_dialog.ui.lineEdit_YC.setText(f'{y_c:.16f}')
        self.set_limits_dialog.ui.lineEdit_deltaX.setText(f'{xmax - xmin:.16f}')
        self.set_limits_dialog.ui.lineEdit_deltaY.setText(f'{ymax - ymin:.16f}')

        self.set_limits_dialog.ui.pushButton_SetLim.clicked.connect(lambda: self.set_limits('xy'))
        self.set_limits_dialog.ui.pushButton_SetC.clicked.connect(lambda: self.set_limits('centre'))
        self.set_limits_dialog.exec()

    def set_limits(self, regime):
        if regime == 'xy':
            lims = self.set_limits_dialog.ui.lineEdit_X.text().split(',')
            xmin, xmax = np.float64(lims)
            lims = self.set_limits_dialog.ui.lineEdit_Y.text().split(',')
            ymin, ymax = np.float64(lims)
        elif regime == 'centre':
            x_centre = np.float64(self.set_limits_dialog.ui.lineEdit_XC.text())
            y_centre = np.float64(self.set_limits_dialog.ui.lineEdit_YC.text())
            delta_x = np.float64(self.set_limits_dialog.ui.lineEdit_deltaX.text())
            delta_y = np.float64(self.set_limits_dialog.ui.lineEdit_deltaY.text())
            xmin = x_centre - delta_x / 2
            xmax = x_centre + delta_x / 2
            ymin = y_centre - delta_y / 2
            ymax = y_centre + delta_y / 2
        else:
            raise ValueError('Invalid regime.')
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)
        self.set_limits_dialog.accept()
        self.set_limits_dialog.deleteLater()
        self.set_limits_dialog = None
