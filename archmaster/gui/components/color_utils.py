from PySide6 import QtGui


class ColorUtils:
    @staticmethod
    def relative_contrast(c: QtGui.QColor, value=150):
        return c.darker(value) if c.lightnessF() > .5 else c.lighter(value)
