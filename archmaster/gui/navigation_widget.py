from PySide6 import QtCore, QtWidgets

from archmaster.chess_game import ChessGame

from .components import ButtonGroupLayout


class NavigationWidget(QtWidgets.QWidget):
    def __init__(self, game: ChessGame, parent):
        super().__init__(parent)

        self.game = game

        layout = ButtonGroupLayout(self)
        layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))

        layout.addStretch()

        layout.addButton('swap_vert', "Flip board", self.game.flip)

        layout.addSpacer()

        layout.addButton(
            'first_page', "Start", self.game.start,
            shortcut=QtCore.Qt.Key.Key_Home)
        layout.addButton(
            'chevron_backward', "Previous move", self.game.previous,
            shortcut=QtCore.Qt.Key.Key_Left)
        layout.addButton(
            'chevron_forward', "Next move", self.game.next,
            shortcut=QtCore.Qt.Key.Key_Right)
        layout.addButton(
            'last_page', "End", self.game.end,
            shortcut=QtCore.Qt.Key.Key_End)

        layout.addStretch()
