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

P_DRAW = """
[Event "Tata Steel India Blitz"]
[Site "Kolkata IND"]
[Round "17.1"]
[Date "2026.1.11"]
[White "Vidit, Santosh Gujrathi"]
[Black "Anand, Viswanathan"]
[WhiteElo "2708"]
[BlackElo "2743"]
[Result "1/2-1/2"]

1.Nf3 d5 2.b3 c5 3.e3 Nf6 4.Bb2 e6 5.Bb5+ Bd7 6.Be2 Nc6 7.O-O Be7 8.d4 cxd4 9.Nxd4 O-O 10.Nd2 Nxd4 11.Bxd4 a5 12.c4 a4 13.cxd5 Nxd5 14.Bf3 Bc6 15.Nc4 Bf6 16.Ne5 axb3 17.axb3 Rxa1 18.Qxa1 Bxe5 19.Bxe5 f6 20.Bd4 Qe7 21.Rc1 1/2-1/2
"""  # noqa
P_TEST = """
[Event "rated rapid game"]
[Site "https://lichess.org/15RlCcxv"]
[Date "2026.09.28"]
[Round "-"]
[White "Side93"]
[Black "fatypunk"]
[Result "1-0"]
[GameId "15RlCcxv"]
[UTCDate "2026.09.28"]
[UTCTime "18:23:23"]
[WhiteElo "1743"]
[BlackElo "1687"]
[WhiteRatingDiff "+4"]
[BlackRatingDiff "-119"]
[Variant "Standard"]
[TimeControl "900+10"]
[ECO "A13"]
[Opening "English Opening: Agincourt Defense"]
[Termination "Normal"]
[Annotator "lichess.org"]

1. c4 e6 { A13 English Opening: Agincourt Defense } 2. g3 d5 3. d4 c5 4. Nf3 Nc6 5. cxd5 exd5 6. dxc5 Bxc5 7. Bg2 Nf6 8. O-O O-O 9. Nc3 d4 10. Nb5?! { (-0.11 → -0.68) Inaccuracy. Na4 was best. } (10. Na4 Be7 11. a3 Bf5 12. b4 Be4 13. Qb3 Nd7 14. b5 Na5 15. Qd1 Re8) 10... a6 11. Na3 Be6 12. Qc2?! { (-0.50 → -1.38) Inaccuracy. Nc2 was best. } (12. Nc2 Bf5 13. b4 Ba7 14. Bb2 d3 15. exd3 Bxd3 16. Bxf6 gxf6 17. Re1 Bg6) 12... Qd6? { (-1.38 → -0.24) Mistake. Ba7 was best. } (12... Ba7 13. b3 Re8 14. Bb2 Qe7 15. Rad1 Rad8 16. Qc1 Ne4 17. Nc2 Nc3 18. Bxc3) 13. Bf4 Ne5?? { (-0.31 → 5.99) Blunder. Qe7 was best. } (13... Qe7 14. Rac1 Ba7 15. Nc4 Rad8 16. Nce5 Bd5 17. Nxc6 Bxc6 18. Bg5 Bb5 19. Bxf6) 14. Bxe5 Qb6 15. Nc4 Bxc4 16. Qxc4 Rac8 17. Qb3 Ne4 18. Qxb6 Bxb6 19. Bxd4 Nd2 20. Bxb6 Nxf1 21. Kxf1 { Black resigns. } 1-0
"""  # noqa
P_LOOSE = """
[Event "Live Chess"]
[Site "Chess.com"]
[Date "2026.10.10"]
[Round "?"]
[White "fatypk"]
[Black "Ryan228665"]
[Result "0-1"]
[TimeControl "900+10"]
[WhiteElo "880"]
[BlackElo "1031"]
[Termination "Ryan228665 a gagné par échec et mat"]
[ECO "D06"]
[EndTime "7:01:22 GMT+0000"]
[Link "https://www.chess.com/game/live/185095202328?username=fatypk&move=0"]

1. d4 d5 2. c4 Nf6 3. cxd5 Qxd5 4. Nc3 Qa5 5. Bd2 Nd5 6. e4 Nxc3 7. Bxc3 Qb6 8.
e5 Bf5 9. Nf3 h6 10. Bc4 e6 11. O-O Bb4 12. a3 Bxc3 13. bxc3 Nc6 14. Rb1 Qa5 15.
Qb3 Bxb1 16. Rxb1 O-O-O 17. Qxb7+ Kd7 18. Bb5 Qb6 19. Bxc6+ Qxc6 20. Qxa7 Qxc3
21. Qa4+ Qc6 22. Qb3 Rb8 23. d5 exd5 24. Nd4 Rxb3 25. Nxc6 Rxb1# 0-1
""" # noqa


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

        self.chess_game = ChessGame(P_TEST)

        self.main_widget = Splitter()
        self.main_widget.setOrientation(
            QtCore.Qt.Orientation.Horizontal
            if self.options.split_horizontal else
            QtCore.Qt.Orientation.Vertical)
        self.board_panel = QtWidgets.QWidget()
        self.data_panel = DataPanel(self.chess_game, self)
        self.data_panel.setVisible(self.options.data_panel)
        self.main_widget.addWidget(self.board_panel)
        self.main_widget.addWidget(self.data_panel)

        layout = QtWidgets.QVBoxLayout(self.board_panel)
        self.board_widget = ChessboardWidget(self.chess_game, self)
        layout.addWidget(self.board_widget)
        self.navigation_widget = NavigationWidget(self.chess_game, self)
        layout.addWidget(self.navigation_widget)
        layout.addStretch()

        self.setCentralWidget(self.main_widget)

        menu = self.menuBar()

        file_menu = menu.addMenu(_("File"))

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


@dataclass
class UIOptions(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!UIOptions"

    fullscreen: bool = False
    window_size: dict = field(
        default_factory=lambda: dict(width=800, height=800))
    split_horizontal: bool = True
    data_panel: bool = True
