from PySide6.QtWidgets import QDialog, QMessageBox


class BaseDialog(QDialog):
    def __init__(self, ui_class, parent=None):
        super().__init__(parent)
        try:
            self.ui = ui_class()
            self.ui.setupUi(self)
        except Exception as e:
            print(f"Error setting up UI: {e}")
            QMessageBox.critical(self, "Error", "Failed to load UI.")


# Constants for default values
DEFAULT_MODE = 'mandelbrot'
DEFAULT_HORIZON_MANDELBROT = 2e35
DEFAULT_HORIZON_JULIA = 4
DEFAULT_POWER = 2
DEFAULT_COLOURMAP = 'jet'
DEFAULT_HEIGHT = 1000
DEFAULT_LENGTH = 1000
DEFAULT_REGIME = 'standard'
DEFAULT_FREQ = 0.01
DEFAULT_OFFSET = 0.0
DEFAULT_C_VIEW = 'xy'
DEFAULT_X_C = -0.8000
DEFAULT_Y_C = -0.1560
DEFAULT_DELTA_SLIDER_C = 5e-4  # 2 / 4000 = (1 - (-1)) / 4000
LIMS_MANDELBROT_DICT = {'2': (-2, 0.5, -1.25, 1.25), '3': (-1, 1, -1.35, 1.35),
                        '4': (-1.35, 1, -1.25, 1.25), '5': (-1, 1, -1, 1),
                        '6': (-1.3, 1.2, -1.2, 1.2), '7': (-1.25, 1.25, -1.3, 1.3),
                        '8': (-1.25, 1.25, -1.3, 1.3)}
