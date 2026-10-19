from dataclasses import dataclass, field

import yaml
from PySide6 import QtCore, QtGui, QtWidgets

from archmaster.chess_game import ChessGame
from archmaster.resources import resources
from archmaster.translations import gettext as _

from .board.chessboard_widget import ChessboardWidget
from .components import Splitter
from .data_panel import DataPanel
from .navigation_widget import NavigationWidget

all_files = _("All files")


class MainWindow(QtWidgets.QMainWindow):
    ui_options_file = resources.user_dir / 'ui_options.yaml'

    def __init__(self):
        super().__init__()

        self.options: UIOptions = resources.load_yaml(
            self.ui_options_file, UIOptions)

        self.setWindowTitle("Archmaster Chess")
        self.resize(
            self.options.window_size['width'],
            self.options.window_size['height'])
        self.layout_mode = 'hozizontal'

        self.game = ChessGame()

        self.main_widget = Splitter()
        self.main_widget.setOrientation(
            QtCore.Qt.Orientation.Horizontal
            if self.options.split_horizontal else
            QtCore.Qt.Orientation.Vertical)
        self.board_panel = QtWidgets.QWidget()
        self.data_panel = DataPanel(self.game, self)
        self.data_panel.setVisible(self.options.data_panel)
        self.main_widget.addWidget(self.board_panel)
        self.main_widget.addWidget(self.data_panel)

        layout = QtWidgets.QVBoxLayout(self.board_panel)
        self.board_widget = ChessboardWidget(self.game, self)
        layout.addWidget(self.board_widget)
        self.navigation_widget = NavigationWidget(self.game, self)
        layout.addWidget(self.navigation_widget)
        layout.addStretch()

        self.setCentralWidget(self.main_widget)

        menu = self.menuBar()

        file_menu = menu.addMenu(_("File"))

        action = QtGui.QAction(_("Open PGN file…"), self)
        action.triggered.connect(self.open_pgn_file)
        file_menu.addAction(action)

        file_menu.addSeparator()

        action = QtGui.QAction(_("Exit"), self)
        action.triggered.connect(self.close)
        file_menu.addAction(action)

        view_menu = menu.addMenu(_("View"))

        action = QtGui.QAction(_("Data panel"), self)
        action.triggered.connect(self.toggle_data_panel)
        action.setShortcut(QtCore.Qt.Key.Key_F1)
        action.setCheckable(True)
        action.setChecked(self.options.data_panel)
        view_menu.addAction(action)

        view_menu.addSeparator()

        action = QtGui.QAction(_("Fullscreen"), self)
        action.triggered.connect(self.toggle_fullscreen)
        action.setShortcut(QtCore.Qt.Key.Key_F11)
        action.setCheckable(True)
        action.setChecked(self.options.fullscreen)
        view_menu.addAction(action)
        if self.options.fullscreen:
            self.showFullScreen()

    def toggle_fullscreen(self):
        self.options.fullscreen = not self.options.fullscreen
        if self.options.fullscreen:
            self.options.window_size = dict(
                width=self.width(), height=self.height())
            self.showFullScreen()
        else:
            self.showNormal()

    def toggle_data_panel(self):
        self.options.data_panel = not self.options.data_panel
        self.data_panel.setVisible(self.options.data_panel)

    def split_horizontal(self):
        self.options.split_horizontal = True
        self.main_widget.setOrientation(QtCore.Qt.Orientation.Horizontal)

    def split_vertical(self):
        self.options.split_horizontal = False
        self.main_widget.setOrientation(QtCore.Qt.Orientation.Vertical)

    def closeEvent(self, event):
        if not self.options.fullscreen:
            self.options.window_size = dict(
                width=self.width(), height=self.height())
        resources.dump_yaml(self.ui_options_file, self.options)
        return super().closeEvent(event)

    def open_pgn_file(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)

        file_dialog.setNameFilters(['PGN (*.pgn)', f'{all_files} (*.*)'])
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            with open(selected_files[0], "r") as stream:
                self.game.load_pgn(stream.read())


@dataclass
class UIOptions(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!UIOptions"

    fullscreen: bool = False
    window_size: dict = field(
        default_factory=lambda: dict(width=800, height=800))
    split_horizontal: bool = True
    data_panel: bool = True
