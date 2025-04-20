import json

import numpy as np
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPainter, QBrush, QMouseEvent, QLinearGradient
from PySide6.QtWidgets import QWidget, QColorDialog, QFileDialog
from matplotlib import colors

from config import BaseDialog
from ui_form_setGradient import Ui_setGradient
from ui_form_setShading import Ui_setShading


class DialogSetShading(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(Ui_setShading)
        ui = self.ui
        if parent.shading:
            ui.lineEdit_azimuth.setText(str(parent.azdeg))
            ui.lineEdit_altitude.setText(str(parent.altdeg))
            ui.lineEdit_vert_exag.setText(str(parent.vert_exag))
        else:
            ui.lineEdit_azimuth.setText('315')
            ui.lineEdit_altitude.setText('5')
            ui.lineEdit_vert_exag.setText('1')
        ui.pushButton_setShading.clicked.connect(parent.set_shading)


class DialogSetGradient(BaseDialog):
    def __init__(self, points=None, parent=None):
        super().__init__(Ui_setGradient)
        ui = self.ui
        self.GradWidget = Gradient(points)
        ui.gridLayout.removeWidget(ui.GradWidget)
        ui.gridLayout.addWidget(self.GradWidget, 1, 0, 1, 4)
        ui.pushButton_Apply.clicked.connect(parent.create_and_set_colourmap)
        ui.pushButton_Reverse.clicked.connect(self.GradWidget.reverse_gradient)
        ui.pushButton_Save.clicked.connect(parent.save_colourmap)
        ui.pushButton_Load.clicked.connect(parent.load_colourmap)


class Gradient(QWidget):
    """
    Widget for creating and editing gradient color maps.
    """

    def __init__(self, points=None, parent=None):
        super().__init__(parent)

        # [(ID, position [0-1], QColor)]
        if points is None:
            self.points = [(1, 0.0, QColor(255, 0, 0)), (2, 1.0, QColor(0, 0, 255))]  # red and blue
        else:
            self.points = points
        self.dragging_index = None
        self.radius = 5

    def paintEvent(self, event):  # parent method, run by self.update()
        painter = QPainter(self)
        gradient = self.make_gradient()
        painter.fillRect(self.rect(), QBrush(gradient))

        # draw control points
        for i, (_, pos, _) in enumerate(self.points):
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
            for i, (_, pos, _) in enumerate(self.points):
                px = pos * self.width()
                if abs(px - x) <= self.radius:
                    if len(self.points) > 2:  # min 2 points
                        del self.points[i]
                        self.update()
                    return

        # check if clicked on existing point
        for pid, pos, _ in self.points:
            px = pos * self.width()
            if abs(px - x) <= self.radius:
                self.dragging_index = pid
                return

        # otherwise, add a new point
        pos = x / self.width()
        colour = QColorDialog.getColor()
        self.activateWindow()
        self.raise_()
        if colour.isValid():
            pid = self.generate_id()
            self.points.append((pid, pos, colour))
            self.points.sort(key=lambda t: t[1])
            self.update()

    def generate_id(self):
        if not self.points:
            return 1
        else:
            return max(p[0] for p in self.points) + 1

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging_index is not None:
            x = event.position().x()
            new_pos = max(0.0, min(1.0, x / self.width()))  # check for out-of-bounds
            new_points = []
            for pid, pos, colour in self.points:
                if pid == self.dragging_index:
                    new_points.append((pid, new_pos, colour))
                else:
                    new_points.append((pid, pos, colour))

            self.points = sorted(new_points, key=lambda t: t[1])
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.dragging_index = None

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        # on double click: change colour if clicked on a point
        x = event.position().x()
        for i, (pid, pos, colour) in enumerate(self.points):
            px = pos * self.width()
            if abs(px - x) <= self.radius:
                new_colour = QColorDialog.getColor(initial=colour)
                self.activateWindow()
                self.raise_()
                if new_colour.isValid():
                    self.points[i] = (pid, pos, new_colour)
                    self.update()
                return

    def make_gradient(self):
        gradient = QLinearGradient(0, 0, self.width(), 0)
        for _, pos, colour in sorted(self.points):
            gradient.setColorAt(pos, colour)
        return gradient

    def reverse_gradient(self):
        for i, (pid, pos, colour) in enumerate(self.points):
            pos = 1 - pos
            self.points[i] = (pid, pos, colour)
        self.points.sort(key=lambda t: t[1])
        self.update()

    def make_colourmap(self):
        colours = []
        for _, pos, colour in self.points:
            colours.append((pos, (colour.red() / 255.0, colour.green() / 255.0, colour.blue() / 255.0, 1.0)))  # RGBA
        if colours[0][0] > 0.0:
            colours.insert(0, (0.0, colours[0][1]))  # Reuse first colour
        if colours[-1][0] < 1.0:
            colours.append((1.0, colours[-1][1]))  # Reuse last colour
        return colors.LinearSegmentedColormap.from_list(name='user_defined_cmap', colors=colours)

    def save_to_file(self, path):
        colours_data = []
        for _, pos, colour in self.points:
            colours_data.append({'position': pos, 'r': colour.red() / 255.0,
                                 'g': colour.green() / 255.0, 'b': colour.blue() / 255.0})

        with open(path, 'w') as f:
            json.dump(colours_data, fp=f, indent=2)

    def load_from_file(self, path):
        with open(path, 'r') as f:
            colours_data = json.load(f)

        self.points.clear()

        for item in colours_data:
            pos = float(item['position'])
            r = round(float(item['r']) * 255)
            g = round(float(item['g']) * 255)
            b = round(float(item['b']) * 255)
            colour = QColor(r, g, b)
            pid = self.generate_id()
            self.points.append((pid, pos, colour))

        self.points.sort(key=lambda t: t[1])
        self.update()


class ColourManager:
    def colourmap_update(self):
        if self.ui.comboBox_Colourmap.currentIndex() == self.ui.comboBox_Colourmap.count() - 1:
            self.gradient_dialog = DialogSetGradient(self.user_defined_colourmap, self)
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
        self.user_defined_colourmap = self.gradient_dialog.GradWidget.points
        if not self.no_ax_update:
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

        if fname:
            self.gradient_dialog.GradWidget.save_to_file(fname)

    def load_colourmap(self):
        fname = QFileDialog.getOpenFileName(self, caption='Choose a filename to load from',
                                            filter='json(*.json)')[0]
        if fname:
            self.gradient_dialog.GradWidget.load_from_file(fname)

    def show_set_shading_dialog(self):
        self.shading_dialog = DialogSetShading(self)
        self.shading_dialog.show()

    def set_shading(self):
        self.shading = True
        self.azdeg = float(self.shading_dialog.ui.lineEdit_azimuth.text())
        self.altdeg = float(self.shading_dialog.ui.lineEdit_altitude.text())
        # Clamp values to (0, 360) and (0, 90)
        self.azdeg = max(0.0, min(360.0, self.azdeg))
        self.altdeg = max(0.0, min(90.0, self.altdeg))
        self.vert_exag = float(self.shading_dialog.ui.lineEdit_vert_exag.text())
        self.ax_update()

    def remove_shading(self):
        if not self.shading:
            pass
        else:
            self.shading = False
            self.ax_update()

    def set_regime(self):
        regime = self.ui.comboBox_regime.currentText()
        if self.regime == regime:
            return
        self.regime = self.ui.comboBox_regime.currentText()
        if regime == 'standard':
            self.cache = None
            self.ui.lineEdit_freq.setVisible(False)
            self.ui.label_freq.setVisible(False)
            self.ui.lineEdit_offset.setVisible(False)
            self.ui.label_offset.setVisible(False)
        elif regime == 'sin':
            self.ui.lineEdit_freq.setVisible(True)
            self.ui.label_freq.setVisible(True)
            self.ui.lineEdit_offset.setVisible(True)
            self.ui.label_offset.setVisible(True)
        if not self.no_ax_update:
            self.ax_update()

    def set_freq(self):
        self.freq = float(self.ui.lineEdit_freq.text())
        data = (np.sin(self.cache * self.freq + self.offset)) ** 2
        im = self.ax.images[0]
        im.set_array(data)
        im.set(clim=(im.get_array().min(), im.get_array().max()))
        self.fig.canvas.draw_idle()

    def set_offset(self):
        self.offset = float(self.ui.lineEdit_offset.text())
        data = (np.sin(self.cache * self.freq + self.offset)) ** 2
        im = self.ax.images[0]
        im.set_array(data)
        im.set(clim=(im.get_array().min(), im.get_array().max()))
        self.fig.canvas.draw_idle()
