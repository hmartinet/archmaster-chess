from PySide6 import QtWidgets

from archmaster.chess_game import ChessGame

from .components import ButtonGroupLayout
from .explorer_widget import ExplorerWidget


class DataPanel(QtWidgets.QWidget):
    def __init__(self, game: ChessGame, parent=None):
        super().__init__(parent)

        self.main_window = parent
        self.game = game

        layout = QtWidgets.QVBoxLayout(self)

        self.explorer_widget = ExplorerWidget(self.game, self)
        layout.addWidget(self.explorer_widget, 1)

        btns = ButtonGroupLayout(icon_size=20).asFrame(noMargins=True)
        self.btn_vertical: QtWidgets.QPushButton = btns.layout().addButton(
            'dock_to_bottom', "Dock to bottom",
            self.split_vertical)
        self.btn_horizontal: QtWidgets.QPushButton = btns.layout().addButton(
            'dock_to_left', "Dock to right",
            self.split_horizontal)
        if self.parent().split_horizontal:
            self.btn_horizontal.hide()
        else:
            self.btn_vertical.hide()
        btns.layout().addStretch()
        layout.addWidget(btns, 0)

    def split_vertical(self):
        self.main_window.split_vertical()
        self.btn_horizontal.show()
        self.btn_vertical.hide()

    def split_horizontal(self):
        self.main_window.split_horizontal()
        self.btn_horizontal.hide()
        self.btn_vertical.show()
