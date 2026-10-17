

from dataclasses import dataclass

import chess
from PySide6 import QtCore, QtGui, QtWidgets
from qt_material_icons import MaterialIcon

from archmaster.chess_game import ChessGame
from archmaster.resources import resources

from .chessboard_painter import ChessboardPainter
from .palette import Palette
from .pieces import Pieces

ROWS = "87654321"
COLS = "abdcedfg"
carlito_path = resources.font_dir / "Carlito" / "Carlito-Bold.ttf"


@dataclass(frozen=True)
class Metrics:
    margin: int
    board_size: int
    full_size: int
    square_size: int
    x_offset: int
    y_offset: int


@dataclass(frozen=False)
class Item:
    name: str
    id: int
    path: QtGui.QPainterPath
    pos: QtCore.QPointF

    def isEqual(self, name, id=None):
        return self.name == name and (
            id is None or self.id == id)


class ChessboardWidget(QtWidgets.QWidget):
    # LIGHT_SQUARE = QtGui.QColor("#F0D9B5")
    # DARK_SQUARE = QtGui.QColor("#B58863")
    BADGES = {
        'win': 'crown',
        'lost': 'hand_gesture',
        'draw': 'balance',
        'checkmate': 'skull',
        'stalemate': 'lock',
        'insufficient_material': 'all_inclusive',  # infinite symbol
        'seventyfive_moves': 'functions',  # sum symbol
        'fivefold_repetition': 'repeat',
    }
    BADGE_COLORS = {
        'win': 'win',
        'lost': 'lost',
        'draw': 'draw',
        'checkmate': 'lost',
        'stalemate': 'draw',
        'insufficient_material': 'draw',
        'seventyfive_moves': 'draw',
        'fivefold_repetition': 'draw',
    }

    def __init__(self, game: ChessGame, parent=None):
        self.selected_square: int = None
        self.clickable_items: list[Item] = []
        self.pressed_item: Item = None

        super().__init__(parent)

        self.game = game
        self.palette = Palette()

        self.setMinimumSize(320, 320)
        policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

        self.pieces = Pieces('tatiana')

        self.font = QtGui.QFontDatabase.applicationFontFamilies(
            QtGui.QFontDatabase.addApplicationFont(str(carlito_path)))[0]

        self.update_metrics()
        self.update_board_data()

        self.game.view_changed.connect(
            self.update)

        self.game.current_node_changed.connect(
            self.update_board_data)

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return self.minimumSize()

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return width

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_metrics()

    def update_board_data(self):
        board = self.game.board
        meta = self.game.board_metadata()
        squares = {}
        move = []
        if board.move_stack:
            last_move = board.peek()
            move.extend([last_move.from_square, last_move.to_square])

        for i in range(64):
            row = 7 - chess.square_rank(i)
            col = chess.square_file(i)
            piece = board.piece_map().get(i)
            piece_meta = None
            if piece:
                symbol = piece.symbol()
                piece_meta = meta.get('pieces', {}).get(symbol)
            squares[i] = {
                'coord': (row, col),
                'tone': (row + col) % 2 == 0 and 'light' or 'dark',
                'move': i in move,
                'piece': piece and symbol,
                'meta': piece_meta,
            }
        self.board_data = squares
        self.update()

    def update_metrics(self):
        base_size = min(self.width(), self.height())
        margin = 20

        board_size = 8 * ((base_size - 2 * margin) // 8)
        full_size = board_size + 2 * margin
        square_size = board_size / 8

        x_offset = (self.width() - full_size) // 2
        y_offset = 0

        self.metrics = Metrics(
            margin=margin, board_size=board_size, full_size=full_size,
            square_size=square_size, x_offset=x_offset, y_offset=y_offset)
        self.update()

    def createLayer(self, color: QtGui.QColor) -> tuple[
            QtGui.QPixmap, QtGui.QPainter]:
        layer = QtGui.QPixmap(self.metrics.full_size, self.metrics.full_size)
        layer.fill(color)
        painter = ChessboardPainter(layer)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        return layer, painter

    def drawCoordinates(self, painter: QtGui.QPainter):
        painter.save()
        align = (
            QtCore.Qt.AlignmentFlag.AlignHCenter |
            QtCore.Qt.AlignmentFlag.AlignVCenter)
        painter.setFont(QtGui.QFont(self.font, 10))
        painter.setPen(self.palette.BOARD_LIGHT.darker(150))
        number_margin = 18
        for i in range(8):
            if self.game.white_oriented:
                num = str(8 - i)
                letter = chr(i + 97)
            else:
                num = str(i + 1)
                letter = chr(104 - i)
            painter.drawText(QtCore.QRectF(
                self.metrics.margin + i * self.metrics.square_size,
                self.metrics.margin - number_margin,
                self.metrics.square_size, number_margin), align, letter)
            painter.drawText(QtCore.QRectF(
                self.metrics.margin + i * self.metrics.square_size,
                self.metrics.margin + self.metrics.board_size,
                self.metrics.square_size, number_margin), align, letter)
            painter.drawText(QtCore.QRectF(
                self.metrics.margin - number_margin,
                self.metrics.margin + i * self.metrics.square_size,
                number_margin, self.metrics.square_size), align, num)
            painter.drawText(QtCore.QRectF(
                self.metrics.margin + self.metrics.board_size,
                self.metrics.margin + i * self.metrics.square_size,
                number_margin, self.metrics.square_size), align, num)
        painter.restore()

    def paintEvent(self, event):
        self.clickable_items = []

        layer0, painter0 = self.createLayer(self.palette.BOARD_LIGHT)
        layer1, painter1 = self.createLayer(QtCore.Qt.GlobalColor.transparent)
        layer2, painter2 = self.createLayer(QtCore.Qt.GlobalColor.transparent)

        self.drawCoordinates(painter0)

        for square, cell in self.board_data.items():
            row, col = cell['coord']
            if not self.game.white_oriented:
                row = 7 - row
                col = 7 - col
            x = col * self.metrics.square_size
            y = row * self.metrics.square_size
            rect = QtCore.QRectF(
                x + self.metrics.margin, y + self.metrics.margin,
                self.metrics.square_size, self.metrics.square_size)

            move = cell['move']
            if self.pressed_item:
                if self.pressed_item.isEqual('square', square):
                    move = True
            elif self.selected_square == square:
                move = True
            back = 'MOVE' if move else 'BOARD'

            painter0.setRenderHint(
                QtGui.QPainter.RenderHint.Antialiasing, False)
            painter0.drawCell(
                rect, getattr(
                    self.palette, f'{back}_{cell['tone']}'.upper()),
                ChessboardPainter.CELL_EFFECT_VOLUME)
            painter0.setRenderHint(
                QtGui.QPainter.RenderHint.Antialiasing, True)
            abs_rect = rect.translated(
                self.metrics.x_offset, self.metrics.y_offset)
            self.clickable_items.append(Item(
                name='square', id=square, path=abs_rect,
                pos=abs_rect.center()))

            symbol = cell['piece']
            if symbol:
                renderer = self.pieces[symbol]
                inset = self.metrics.square_size / 32
                piece_size = self.metrics.square_size - 2 * inset
                if (self.pressed_item and
                        self.pressed_item.isEqual('square', square)):
                    drag_pos = self.pressed_item.pos
                    piece_pos = (
                        drag_pos.x() - self.metrics.x_offset - piece_size / 2,
                        drag_pos.y() - self.metrics.y_offset - piece_size / 2)
                else:
                    piece_pos = rect.x() + inset, rect.y() + inset
                renderer.render(painter1, QtCore.QRectF(
                        *piece_pos, piece_size, piece_size))

            if cell['meta']:
                size = 24
                rect_size = 32
                delta = (rect_size - size) / 2
                label_rect = QtCore.QRectF(
                    x + self.metrics.margin +
                    self.metrics.square_size - (2 * rect_size / 3),
                    y + self.metrics.margin - (rect_size / 3),
                    rect_size, rect_size)
                path = QtGui.QPainterPath()
                path.addRoundedRect(label_rect, 2, 2)
                painter2.fillPath(path, getattr(
                    self.palette,
                    f'BADGE_{self.BADGE_COLORS[cell['meta']]}'.upper()))
                painter2.drawPixmap(
                    label_rect.x() + delta + 1, label_rect.y() + delta,
                    MaterialIcon(
                        self.BADGES[cell['meta']],
                        fill=True, size=size).pixmap())

        painter0.end()
        painter1.end()
        painter2.end()

        painter = QtGui.QPainter(self)
        painter.drawPixmap(
            self.metrics.x_offset, self.metrics.y_offset, layer0)
        painter.drawPixmap(
            self.metrics.x_offset, self.metrics.y_offset, layer1)
        painter.drawPixmap(
            self.metrics.x_offset, self.metrics.y_offset, layer2)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)

        painter.end()

    def get_item_at(self, pos: QtCore.QPointF):
        for item in reversed(self.clickable_items):
            if item.path.contains(pos):
                return item
        return None

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() != QtCore.Qt.MouseButton.LeftButton:
            return

        pos = event.position()
        self.pressed_item = self.get_item_at(pos)
        self.update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if event.button() != QtCore.Qt.MouseButton.LeftButton:
            return

        pos = event.position()

        pressed_item = self.pressed_item
        self.pressed_item = None

        item = self.get_item_at(pos)
        if pressed_item and item:
            if pressed_item.isEqual(item.name, item.id):
                getattr(self, f'on_{item.name}_click')(item.id)
            elif pressed_item.isEqual('square') and item.isEqual('square'):
                self.selected_square = pressed_item.id
                getattr(self, f'on_{item.name}_click')(item.id)

        self.update()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if not (event.buttons() & QtCore.Qt.MouseButton.LeftButton):
            return

        if self.pressed_item and self.pressed_item.isEqual('square'):
            self.pressed_item.pos = event.position()
            self.update()

    def on_square_click(self, square):
        if self.selected_square is not None:
            move = chess.Move(self.selected_square, square)
            self.selected_square = None
            legal = self.game.play(move)
            if legal:
                self.update_board_data()
                return

        piece = self.game.board.piece_at(square)
        if piece:
            self.selected_square = square
