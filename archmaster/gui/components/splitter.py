from PySide6 import QtCore, QtGui, QtWidgets

from .color_utils import ColorUtils


class SplitterHandle(QtWidgets.QSplitterHandle):
    def __init__(self, o, parent):
        super().__init__(o, parent)
        self.back_color = ColorUtils.relative_contrast(
            self.palette().window().color(), 200)
        self.highlight_color = ColorUtils.relative_contrast(
            self.palette().window().color(), 400)

    def enterEvent(self, event):
        self.update()
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.update()
        return super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        width = self.rect().width()
        height = self.rect().height()
        painter.setPen(QtGui.QPen(
            self.highlight_color if self.underMouse() else
            self.back_color, 2))

        spacing = 8
        y = -width

        while y < height:
            painter.drawLine(
                QtCore.QPointF(0, y + width),
                QtCore.QPointF(width, y),
            )
            y += spacing


class Splitter(QtWidgets.QSplitter):
    def __init__(self, *args, **kw):
        kw.setdefault('handleWidth', 10)
        super().__init__(*args, **kw)
        self.setChildrenCollapsible(False)

    def createHandle(self):
        return SplitterHandle(self.orientation(), self)
