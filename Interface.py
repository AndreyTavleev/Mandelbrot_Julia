import json
import sys

import matplotlib
import numpy as np
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QIcon, QPalette, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QFileDialog,
                               QMainWindow, QProxyStyle, QStyle, QVBoxLayout)
from matplotlib import colors
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from colour_controls import ColourManager
from config import *
from fractal_calculation import fractal_set
from fractal_controls import (CoordinateManager, FractalControls,
                              ImageRenderer, JuliaParameterControl,
                              polar_coordinates)
from ui_form_MandelbrotJulia import Ui_MainWindowMandelbrotJulia
from ui_form_Save import Ui_Save

matplotlib.use('Qt5Agg')


class CustomSliderStyle(QProxyStyle):
    def styleHint(self, hint, option=None, widget=None, returnData=None):
        if hint == QStyle.SH_Slider_AbsoluteSetButtons:
            return Qt.LeftButton.value
        return super().styleHint(hint, option, widget, returnData)


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)


class CustomToolbar(NavigationToolbar2QT):
    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)
        self.parent = parent
        unwanted_buttons = ['Subplots', 'Customize']
        for action in self.actions():
            if action.text() in unwanted_buttons:
                self.removeAction(action)

    def home(self):
        self.parent.reset_lims()

    def save_figure(self):
        self.parent.show_save_image_dialog()


class DialogSave(BaseDialog):
    def __init__(self, parent: QMainWindow = None):
        super().__init__(Ui_Save)
        ui = self.ui
        ui.lineEdit_L.editingFinished.connect(lambda: parent.edit_size('L'))
        ui.lineEdit_H.editingFinished.connect(lambda: parent.edit_size('H'))
        ui.lineEdit_DPI.editingFinished.connect(parent.edit_size_label)
        ui.checkBox_withAxes.stateChanged.connect(parent.edit_size_label)
        ui.checkBox_lockAR.stateChanged.connect(lambda: parent.edit_size('L'))

        ui.lineEdit_L.setText('1000')
        ui.lineEdit_H.setText('1000')
        ui.lineEdit_DPI.setText(str(int(parent.fig.dpi)))
        ui.lineEdit_DPI.setEnabled(False)

        ui.label_Size.setText('Image size: \n1000 \U000000D7 1000 pix.')

        ui.pushButton_Save.clicked.connect(parent.save_dial)


class MyWindowMandelbrotJulia(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindowMandelbrotJulia()
        self.ui.setupUi(self)


class ImageExporter:
    def save_load(self):
        option = self.ui.comboBox_SaveLoad.currentIndex()
        if option == 0:
            self.show_save_image_dialog()
        elif option == 1:
            fname = QFileDialog.getSaveFileName(self, caption='Choose a filename to save to',
                                                dir='$HOME/Desktop/Metadata.json',
                                                filter='json(*.json)')[0]
            if fname:
                self.save_metadata(fname)
        elif option == 2:
            fname = QFileDialog.getOpenFileName(self, caption='Choose a filename to load from',
                                                filter='json(*.json)')[0]
            if fname:
                self.load_metadata(fname)
        else:
            raise ValueError('Invalid save/load option.')
        self.ui.comboBox_SaveLoad.setCurrentIndex(0)

    def show_save_image_dialog(self):
        self.save_image_dialog = DialogSave(self)
        self.save_image_dialog.exec()

    def save_dial(self):
        filter_save = ('Portable Network Graphics (*.png);; Joint Photographic Expects Group (*jpeg *.jpg);; '
                       'Tagged Image File Format (*.tiff);; Portable Document Format (*.pdf);; '
                       'Encapsulated PostScript (*.eps)')
        fname = QFileDialog.getSaveFileName(self, caption='Choose a filename to save to',
                                            dir='$HOME/Desktop/Image.png',
                                            filter=filter_save)[0]
        if fname:
            self.save_to_file(fname)

    def save_to_file(self, filename):
        self.save_image_dialog.ui.pushButton_Save.setEnabled(False)
        length = int(self.save_image_dialog.ui.lineEdit_L.text())
        height = int(self.save_image_dialog.ui.lineEdit_H.text())
        img_width, img_height = length, height
        if self.save_image_dialog.ui.checkBox_withAxes.isChecked():
            dpi = int(self.save_image_dialog.ui.lineEdit_DPI.text())
            img_width *= dpi
            img_height *= dpi
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        print(xmin, xmax, ymin, ymax, self.x_c, self.y_c, self.horizon)
        data = fractal_set(xmin, xmax, ymin, ymax, x_c=self.x_c, y_c=self.y_c,
                           height=img_height, length=img_width,
                           n=self.n, horizon=self.horizon, power=self.power,
                           mode=self.mode)[2].T
        if self.regime == 'sin':
            data = (np.sin(data * self.freq + self.offset)) ** 2
        if self.save_image_dialog.ui.checkBox_withAxes.isChecked():
            _, ax = plt.subplots(figsize=(length, height), dpi=dpi)
            if not self.shading:
                ax.imshow(data, origin='lower', cmap=self.colourmap, extent=(xmin, xmax, ymin, ymax))
            else:
                light = colors.LightSource(azdeg=self.azdeg, altdeg=self.altdeg)
                data = light.shade(data, cmap=plt.get_cmap(self.colourmap), vert_exag=self.vert_exag,
                                   blend_mode='hsv')
                ax.imshow(data, extent=(xmin, xmax, ymin, ymax), origin='lower')
            ax.tick_params(labelsize='xx-large')
            ax.xaxis.offsetText.set_fontsize('xx-large')
            ax.yaxis.offsetText.set_fontsize('xx-large')
            plt.tight_layout()
            plt.savefig(filename, dpi=dpi)
        else:
            if not self.shading:
                plt.imsave(filename, data, cmap=self.colourmap, origin='lower')
            else:
                light = colors.LightSource(azdeg=self.azdeg, altdeg=self.altdeg)
                data = light.shade(data, cmap=plt.get_cmap(self.colourmap), vert_exag=self.vert_exag,
                                   blend_mode='hsv')
                plt.imsave(filename, data, origin='lower')
        QMessageBox.information(self, 'Save File', f'Image is saved to {filename}')
        self.save_image_dialog.ui.pushButton_Save.setEnabled(True)

    def edit_size_label(self):
        ll = int(self.save_image_dialog.ui.lineEdit_L.text())
        h = int(self.save_image_dialog.ui.lineEdit_H.text())
        if self.save_image_dialog.ui.checkBox_withAxes.isChecked():
            self.save_image_dialog.ui.lineEdit_DPI.setEnabled(True)
            dpi = int(self.save_image_dialog.ui.lineEdit_DPI.text())
            self.save_image_dialog.ui.label_Size.setText(f'Image size: \n{ll * dpi} \U000000D7 {h * dpi} pix.')
        else:
            self.save_image_dialog.ui.lineEdit_DPI.setEnabled(False)
            self.save_image_dialog.ui.label_Size.setText(f'Image size: \n{ll} \U000000D7 {h} pix.')

    def edit_size(self, regime):
        if self.save_image_dialog.ui.checkBox_lockAR.isChecked():
            aspect_ratio = np.diff(self.ax.get_ylim())[0] / np.diff(self.ax.get_xlim())[0]
            aspect_ratio = abs(aspect_ratio)
            if regime == 'L':
                ll = abs(int(self.save_image_dialog.ui.lineEdit_L.text()))
                hh = round(ll * aspect_ratio)
                self.save_image_dialog.ui.lineEdit_H.setText(str(hh))
            elif regime == 'H':
                hh = abs(int(self.save_image_dialog.ui.lineEdit_H.text()))
                ll = round(hh / aspect_ratio)
                self.save_image_dialog.ui.lineEdit_L.setText(str(ll))
            else:
                raise ValueError('Invalid regime.')
        self.edit_size_label()

    def save_metadata(self, path):
        metadata = {'mode': self.mode, 'n': self.n, 'horizon': self.horizon, 'power': self.power}
        if self.mode in {'julia', 'burning_ship_julia'}:
            metadata['x_c'] = self.x_c
            metadata['y_c'] = self.y_c
        metadata['lims_x'] = self.ax.get_xlim()
        if self.mode in {'mandelbrot', 'julia'}:
            metadata['lims_y'] = self.ax.get_ylim()
        elif self.mode in {'burning_ship', 'burning_ship_julia'}:
            metadata['lims_y'] = self.ax.get_ylim()[::-1]
        else:
            raise ValueError('Invalid mode.')
        if self.ui.comboBox_Colourmap.currentIndex() == self.ui.comboBox_Colourmap.count() - 1:
            colourmap = []
            for _, pos, colour in self.user_defined_colourmap:
                colourmap.append({'position': pos, 'r': colour.red() / 255.0,
                                  'g': colour.green() / 255.0, 'b': colour.blue() / 255.0})
            metadata['colourmap'] = colourmap
        else:
            metadata['colourmap'] = self.ui.comboBox_Colourmap.currentText()
        metadata['regime'] = self.regime
        if self.regime == 'sin':
            metadata['freq'] = self.freq
            metadata['offset'] = self.offset
        metadata['shading'] = self.shading
        if self.shading:
            metadata['azdeg'] = self.azdeg
            metadata['altdeg'] = self.altdeg
            metadata['vert_exag'] = self.vert_exag
        with open(path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def load_metadata(self, path):
        with open(path, 'r') as f:
            metadata = json.load(f)
        self.no_ax_update = True  # prevent ax_update until setting all the parameters
        self.ui.comboBox_Set.setCurrentText(metadata['mode'])
        self.ui.comboBox_Set.activated.emit(1)
        if self.mode in {'julia', 'burning_ship_julia'}:
            self.c_view = 'xy'
            slider_xc_val = self.from_value_to_slider(metadata['x_c'], 'xc')
            slider_yc_val = self.from_value_to_slider(metadata['y_c'], 'yc')
            if (slider_xc_val < 0 or slider_xc_val > 4000 or
                    slider_yc_val < 0 or slider_yc_val > 4000):
                self.invalid_slider = True
                self.ui.horizontalSlider_XC.setValue(round(slider_xc_val))
                self.ui.horizontalSlider_YC.setValue(round(slider_yc_val))
                self.invalid_slider = False
                self.set_c_from_values(metadata['x_c'], metadata['y_c'], 'xy')
            else:
                self.ui.horizontalSlider_XC.setValue(round(slider_xc_val))
                self.ui.horizontalSlider_YC.setValue(round(slider_yc_val))
        self.ui.lineEdit_N.setText(str(metadata['n']))
        self.ui.lineEdit_H.setText(str(metadata['horizon']))
        self.ui.comboBox_Power.setCurrentText(str(metadata['power']))
        self.ui.comboBox_Power.activated.emit(1)
        self.ui.pushButton_Rebuild.clicked.emit()
        if isinstance(metadata['colourmap'], str):
            self.ui.comboBox_Colourmap.setCurrentText(metadata['colourmap'])
            self.colourmap = metadata['colourmap']
        else:
            self.user_defined_colourmap = []
            for i, item in enumerate(metadata['colourmap']):
                pos = float(item['position'])
                r = round(float(item['r']) * 255)
                g = round(float(item['g']) * 255)
                b = round(float(item['b']) * 255)
                colour = QColor(r, g, b)
                pid = i + 1
                self.user_defined_colourmap.append((pid, pos, colour))
            self.user_defined_colourmap.sort(key=lambda t: t[1])
            self.ui.comboBox_Colourmap.setCurrentText('Set your own colourmap...')
            self.ui.comboBox_Colourmap.activated.emit(1)
            self.gradient_dialog.ui.pushButton_Apply.clicked.emit()
            self.gradient_dialog.accept()
            self.gradient_dialog.deleteLater()
            self.gradient_dialog = None
        self.shading = metadata['shading']
        if self.shading:
            self.azdeg = metadata['azdeg']
            self.altdeg = metadata['altdeg']
            self.vert_exag = metadata['vert_exag']
            self.azdeg = max(0.0, min(360.0, self.azdeg))
            self.altdeg = max(0.0, min(90.0, self.altdeg))
        self.ui.comboBox_regime.setCurrentText(metadata['regime'])
        if metadata['regime'] == 'sin':
            self.cache = None
            self.freq = metadata['freq']
            self.offset = metadata['offset']
            self.ui.lineEdit_freq.setText(str(self.freq))
            self.ui.lineEdit_offset.setText(str(self.offset))
        self.ui.comboBox_regime.activated.emit(1)
        self.no_ax_update = False
        self.ax.set_xlim(metadata['lims_x'][0], metadata['lims_x'][1])
        self.ax.set_ylim(metadata['lims_y'][0], metadata['lims_y'][1])


class MJSet(MyWindowMandelbrotJulia, FractalControls, CoordinateManager, JuliaParameterControl,
            ColourManager, ImageRenderer, ImageExporter):
    """
    A class for handling graphical user interface rendering, interactions, and state
    management for Mandelbrot and Julia set visualisations.
    """

    def __init__(self, application: QApplication = None, parent=None):
        super().__init__(parent)

        # Initialization
        self.initialize_defaults(application)  # default attributes
        self.initialize_ui_components()  # groupBoxes, comboBoxes
        self.setup_canvas_and_toolbar()  # matplotlib plot and toolbar
        self.update_ui_defaults()  # set the default texts and slider/colourmap values
        self.connect_signals()  # buttonClick, comboBoxActivate, sliderValueChanged

    def initialize_defaults(self, application: QApplication):
        """Sets default values for instance variables."""
        self.application = application
        self.mode = DEFAULT_MODE
        self.horizon = DEFAULT_HORIZON_MANDELBROT
        self.x_c_0, self.y_c_0 = DEFAULT_X_C, DEFAULT_Y_C
        self.rho_c_0, self.phi_c_0 = polar_coordinates(self.x_c_0, self.y_c_0)
        self.x_c, self.y_c = self.x_c_0, self.y_c_0
        self.rho_c, self.phi_c = self.rho_c_0, self.phi_c_0
        self.height, self.length = DEFAULT_HEIGHT, DEFAULT_LENGTH
        self.colourmap, self.power = DEFAULT_COLOURMAP, DEFAULT_POWER
        self.slider_move, self.rebuild, self.shading = False, False, False
        self.azdeg, self.altdeg, self.vert_exag = None, None, None
        self.regime = DEFAULT_REGIME
        self.freq, self.offset = DEFAULT_FREQ, DEFAULT_OFFSET
        self.no_ax_update = False
        self.c_view = DEFAULT_C_VIEW
        self.delta_slider_xc = DEFAULT_DELTA_SLIDER_C
        self.delta_slider_yc = DEFAULT_DELTA_SLIDER_C
        self.invalid_slider = False
        self.cache = None

        # Initialize dialogues and toolbar
        self.main_layout = None
        self.set_limits_dialog, self.save_image_dialog = None, None
        self.set_c_dialog, self.shading_dialog = None, None
        self.gradient_dialog = None
        self.user_defined_colourmap = None
        self.toolbar = None

    def initialize_ui_components(self):
        """Initializes UI components and configures their default values."""
        self.ui.groupbox_C.setVisible(False)
        self.ui.lineEdit_freq.setVisible(False)
        self.ui.label_freq.setVisible(False)
        self.ui.label_offset.setVisible(False)
        self.ui.lineEdit_offset.setVisible(False)
        self.ui.comboBox_Set.addItems(['mandelbrot', 'julia', 'burning_ship', 'burning_ship_julia'])
        self.ui.comboBox_regime.addItems(['standard', 'sin'])
        self.ui.comboBox_Power.addItems([str(i) for i in range(2, 9)])
        self.ui.comboBox_viewC.addItems(['ReC, ImC', '\U000003C1, \U000003D5'])
        self.ui.comboBox_SaveLoad.addItems(['Save image', 'Save metadata', 'Load metadata'])

        for i, cmap in enumerate(plt.colormaps()):
            if i == 0:
                self.ui.comboBox_Colourmap.setIconSize(QPixmap(f'colour_pic/{cmap}.png').scaled(100, 20).size())
            pixmap = QPixmap(f'colour_pic/{cmap}.png').scaled(100, 20)
            icon = QIcon(pixmap)
            self.ui.comboBox_Colourmap.addItem(icon, cmap)
        self.ui.comboBox_Colourmap.addItem('Set your own colourmap...')
        self.ui.comboBox_Colourmap.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.ui.comboBox_Colourmap.setMinimumContentsLength(3)

    def setup_canvas_and_toolbar(self):
        """Sets up the matplotlib canvas and initial plot configuration."""
        self.sc = MplCanvas()
        self.ax, self.fig = self.sc.ax, self.sc.fig
        self.fig.patch.set_facecolor(self.ui.centralwidget.palette().color(QPalette.Window).name())

        # Set the light/dark theme
        if self.application.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            self.ax.tick_params(axis='both', colors='w')
        self.application.styleHints().colorSchemeChanged.connect(
            lambda: QTimer.singleShot(100, self.colour_scheme_changed))

        # origin='lower' is used to match the image coordinates with the plot coordinates
        self.ax.imshow([[0]], origin='lower', cmap=self.colourmap)  # Empty initial image
        self.ax.callbacks.connect('ylim_changed', self.ax_update)
        self.ax.set(xlim=(self.xmin_0, self.xmax_0), ylim=(self.ymin_0, self.ymax_0))
        self.fig.tight_layout()

        self.toolbar = CustomToolbar(self.sc, self)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.sc)
        self.main_layout.addWidget(self.toolbar)
        self.ui.frame.setLayout(self.main_layout)

    def update_ui_defaults(self):
        """Updates UI fields with the default attributes."""
        self.ui.comboBox_Set.setCurrentText(self.mode)
        self.ui.comboBox_Power.setCurrentText(str(self.power))
        self.ui.comboBox_regime.setCurrentText('standard')
        self.ui.comboBox_viewC.setCurrentText('ReC, ImC')
        self.ui.lineEdit_N.setText(f'{self.n}')
        self.ui.lineEdit_H.setText(f'{self.horizon:.1e}')
        self.ui.horizontalSlider_N.setValue(self.n)
        self.ui.comboBox_Colourmap.setCurrentText(self.colourmap)
        self.ui.lineEdit_freq.setText(f'{self.freq:.2f}')
        self.ui.lineEdit_offset.setText(f'{self.offset:.2f}')
        self.ui.label_freq.setText('\U000003C9:')
        self.ui.label_offset.setText('\U00000394:')

        ini_slider_xc_val = self.from_value_to_slider(self.x_c_0, 'xc')
        ini_slider_yc_val = self.from_value_to_slider(self.y_c_0, 'yc')

        self.ui.horizontalSlider_XC.setValue(round(ini_slider_xc_val))
        self.ui.horizontalSlider_YC.setValue(round(ini_slider_yc_val))

        self.ui.label_C.setText(f'C = {self.x_c:.4f} {self.y_c:+.4f}\U0001D456 = '
                                f'{self.rho_c:.4f}\U000022C5exp({self.phi_c:.4f}\U0001D456)')

    def connect_signals(self):
        """Connects signals to their respective slots."""
        self.ui.comboBox_Set.activated.connect(self.mode_update)
        self.ui.comboBox_Colourmap.activated.connect(self.colourmap_update)
        self.ui.comboBox_regime.activated.connect(self.set_regime)
        self.ui.comboBox_viewC.activated.connect(self.change_c_view)
        self.ui.comboBox_SaveLoad.activated.connect(self.save_load)
        self.ui.comboBox_Power.activated.connect(self.set_power)

        self.ui.lineEdit_freq.editingFinished.connect(self.set_freq)
        self.ui.lineEdit_offset.editingFinished.connect(self.set_offset)

        # Coordinate sliders
        self.ui.horizontalSlider_N.valueChanged.connect(self.change_n)
        self.ui.horizontalSlider_XC.valueChanged.connect(self.set_c_from_slider)
        self.ui.horizontalSlider_YC.valueChanged.connect(self.set_c_from_slider)

        # Button actions
        for button, action in (
                (self.ui.pushButton_zoom_plus, lambda: self.zoom('plus')),
                (self.ui.pushButton_zoom_minus, lambda: self.zoom('minus')),
                (self.ui.pushButton_NewLims, self.show_set_limits_dialog),
                (self.ui.pushButton_ResetLims, self.reset_lims),
                (self.ui.pushButton_ResetN, self.reset_n),
                (self.ui.pushButton_ResetC, self.reset_c),
                (self.ui.pushButton_setC, self.show_set_c_dialog),
                (self.ui.pushButton_setShading, self.show_set_shading_dialog),
                (self.ui.pushButton_removeShading, self.remove_shading),
                (self.ui.pushButton_Rebuild, self.rebuild_im),
                (self.ui.pushButton_Reset, self.reset_im),
        ):
            button.clicked.connect(action)

    def colour_scheme_changed(self):
        self.fig.patch.set_facecolor(self.ui.centralwidget.palette().color(QPalette.Window).name())
        if self.application.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            self.ax.tick_params(axis='both', colors='w')
        else:
            self.ax.tick_params(axis='both', colors='k')
        self.fig.canvas.draw_idle()
        self.main_layout.removeWidget(self.toolbar)
        self.toolbar = CustomToolbar(self.sc, self)
        self.main_layout.addWidget(self.toolbar)

    def closeEvent(self, event):
        self.application.closeAllWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(CustomSliderStyle())
    window = MJSet(app)
    window.show()
    sys.exit(app.exec())
