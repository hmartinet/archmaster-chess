from PySide6 import QtCore, QtGui


class ChessboardPainter(QtGui.QPainter):
    CELL_EFFECT_FLAT = 0
    CELL_EFFECT_VOLUME = 1
    CELL_EFFECT_DIAG = 2

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.cell_cache = {}

    def drawCell(self, rect, color: QtGui.QColor, effect):
        if str(color) not in self.cell_cache:
            pixmap = QtGui.QPixmap(rect.width(), rect.width())
            pixmap.fill(QtCore.Qt.GlobalColor.transparent)
            painter = QtGui.QPainter(pixmap)
            match effect:
                case self.CELL_EFFECT_VOLUME:
                    self._drawCellVolume(painter, color)
                case self.CELL_EFFECT_DIAG:
                    self._drawCellDiag(painter, color)
                case _:
                    painter.fillRect(color)
            painter.end()
            self.cell_cache[str(color)] = pixmap
        self.drawPixmap(rect.x(), rect.y(), self.cell_cache[str(color)])

    @staticmethod
    def _drawCellVolume(painter: QtGui.QPainter, color):
        width = painter.viewport().width()
        gradient = QtGui.QLinearGradient(
            painter.viewport().topLeft(),
            painter.viewport().bottomLeft(),
        )
        gradient.setColorAt(0.0, color.lighter(110))
        gradient.setColorAt(1.0, color.darker(110))
        painter.fillRect(painter.viewport(), QtGui.QBrush(gradient))

        edge = width / 20.
        gradients = [(
            # Left
            QtCore.QPointF(0, width / 2),
            QtCore.QPointF(edge, width / 2),
        ), (
            # Right
            QtCore.QPointF(width, width / 2),
            QtCore.QPointF(width - edge, width / 2),
        ), (
            # Top
            QtCore.QPointF(width / 2, 0),
            QtCore.QPointF(width / 2, edge),
        ), (
            # Bottom
            QtCore.QPointF(width / 2, width),
            QtCore.QPointF(width / 2, width - edge),
        )]
        for start, end in gradients:
            gradient = QtGui.QLinearGradient(start, end)
            gradient.setColorAt(0, QtGui.QColor(0, 0, 0, 45))
            gradient.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
            painter.fillRect(painter.viewport(), gradient)

    @staticmethod
    def _drawCellDiag(painter: QtGui.QPainter, color):
        width = painter.viewport().width()
        thick = round(width / 40.)
        painter.setPen(QtGui.QPen(color, thick))

        spacing = thick * 3
        x = -width

        while x < width:
            painter.drawLine(
                QtCore.QPointF(x, width),
                QtCore.QPointF(x + width, 0),
            )
            x += spacing
