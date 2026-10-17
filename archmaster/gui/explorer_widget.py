from PySide6 import QtCore, QtGui, QtQuickWidgets

from archmaster.chess_game import ChessGame
from archmaster.gui.components import ColorUtils
from archmaster.resources import resources


class ExplorerWidget(QtQuickWidgets.QQuickWidget):
    def __init__(self, game: ChessGame, parent=None):
        super().__init__(parent)

        palette = self.palette()
        self.setClearColor(palette.color(QtGui.QPalette.ColorRole.Window))

        self.rootContext().setContextProperty("theme", {
            "window": palette.color(QtGui.QPalette.ColorRole.Window),
            "window_hover": ColorUtils.relative_contrast(
                palette.color(QtGui.QPalette.ColorRole.Window), 200),
            "mid": palette.color(QtGui.QPalette.ColorRole.Mid),
            "midlight": palette.color(QtGui.QPalette.ColorRole.Midlight),
            "text": palette.color(QtGui.QPalette.ColorRole.WindowText),
            "text_inactive": palette.color(
                QtGui.QPalette.ColorGroup.Inactive,
                QtGui.QPalette.ColorRole.WindowText),
            "text_disabled": palette.color(
                QtGui.QPalette.ColorGroup.Disabled,
                QtGui.QPalette.ColorRole.WindowText),
            "base": palette.color(QtGui.QPalette.ColorRole.Base),
            "baseText": palette.color(QtGui.QPalette.ColorRole.Text),
            "alternateBase": palette.color(
                QtGui.QPalette.ColorRole.AlternateBase),
            "bright": palette.color(QtGui.QPalette.ColorRole.BrightText),
            "highlight": palette.color(QtGui.QPalette.ColorRole.Highlight),
            "highlightedText": palette.color(
                QtGui.QPalette.ColorRole.HighlightedText),
            "highlightedText_disabled": palette.color(
                QtGui.QPalette.ColorGroup.Disabled,
                QtGui.QPalette.ColorRole.HighlightedText),
            "button": palette.color(QtGui.QPalette.ColorRole.Button),
            "buttonText": palette.color(QtGui.QPalette.ColorRole.ButtonText),
        })

        self.game = game
        self.rootContext().setContextProperty("game", self.game)

        self.setMinimumWidth(320)
        self.setMinimumHeight(100)
        self.setResizeMode(
            QtQuickWidgets.QQuickWidget.ResizeMode.SizeViewToRootObject
        )

        qml_file = resources.qml_dir / 'explorer' / 'Explorer.qml'
        self.setSource(QtCore.QUrl.fromLocalFile(str(qml_file)))
