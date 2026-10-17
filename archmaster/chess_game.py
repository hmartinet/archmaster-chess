import io
from dataclasses import dataclass

import chess.pgn
from PySide6.QtCore import Property, QObject, Signal, Slot

RESULT_COLORS = {
    '1-0': chess.WHITE,
    '0-1': chess.BLACK,
    '1/2-1/2': None,
}


@dataclass(frozen=True)
class MoveItem:
    ply: int
    san: str
    uci: str


class ChessGame(QObject):
    view_changed = Signal()
    current_node_changed = Signal()
    tree_changed = Signal()

    def __init__(self, pgn: str | None = None):
        super().__init__()
        self.game = (
            chess.pgn.read_game(io.StringIO(pgn)) if pgn
            else chess.pgn.Game()
        )
        if self.game is None:
            raise ValueError("Invalid or empty PGN")

        self.current_node = self.game
        self.node_index = {}

        self.white_oriented = True

    @property
    def board(self):
        return self.current_node.board()

    def flip(self):
        self.white_oriented = not self.white_oriented
        self.view_changed.emit()

    def next(self):
        if self.current_node.variations:
            self.current_node = self.current_node.variations[0]
            self.current_node_changed.emit()

    def previous(self):
        if self.current_node.parent:
            self.current_node = self.current_node.parent
            self.current_node_changed.emit()

    def start(self):
        self.current_node = self.game
        self.current_node_changed.emit()

    def end(self):
        node = self.current_node
        while node.variations:
            node = node.variations[0]

        if node != self.current_node:
            self.current_node = node
            self.current_node_changed.emit()

    def play(self, move: chess.Move):
        if not self.board.is_legal(move):
            return False

        for variation in self.current_node.variations:
            if variation.move == move:
                self.current_node = variation
                self.current_node_changed.emit()
                return True

        self.current_node = self.current_node.add_variation(move)
        self.tree_changed.emit()
        self.current_node_changed.emit()
        return True

    def _add_termination_meta(self, meta, winner, termination=None):
        lost_label = (
            'checkmate' if termination == chess.Termination.CHECKMATE
            else 'lost')
        if winner == chess.WHITE:
            meta.setdefault('pieces', {})['K'] = 'win'
            meta.setdefault('pieces', {})['k'] = lost_label
        elif winner == chess.BLACK:
            meta.setdefault('pieces', {})['K'] = lost_label
            meta.setdefault('pieces', {})['k'] = 'win'
        else:
            draw_label = termination.name.lower() if termination else 'draw'
            meta.setdefault('pieces', {})['K'] = draw_label
            meta.setdefault('pieces', {})['k'] = draw_label

    def board_metadata(self):
        meta = {}

        outcome = self.board.outcome()
        if outcome:
            self._add_termination_meta(
                meta, outcome.winner, outcome.termination)
        else:
            is_last_move = self.current_node == self.game.end()
            result = self.game.headers.get("Result")
            if is_last_move and result in RESULT_COLORS:
                self._add_termination_meta(meta, RESULT_COLORS[result])
        return meta

    @Property(str, notify=current_node_changed)
    def current_node_id(self):
        return str(id(self.current_node))

    @Slot(str)
    def set_current_node_id(self, node_id):
        node = self.node_index.get(node_id)
        if node is not None:
            self.current_node = node
            self.current_node_changed.emit()

    @Property(list, notify=tree_changed)
    def tree(self):
        self.node_index = {}

        def build_move(node, bloc_list):
            ply = node.ply()
            node_id = str(id(node))
            self.node_index[node_id] = node
            full_move = (ply + 1) // 2
            dots = '.' if ply % 2 else '....'
            return {
                "type": "move",
                "ply": ply,
                "fm":  (
                    f"{full_move}{dots}"
                    if (ply % 2 or not bloc_list) else ''),
                "san": node.san(),
                "uci": node.uci(),
                "id": node_id,
            }

        def new_list(list_type, items=None):
            return {
                "type": list_type,
                "items": items or []}

        def build_line(node):
            line = []
            move_list = new_list("move_list")

            if node.move:
                move_list["items"].append(
                    build_move(node, move_list["items"]))

            while node.variations:
                mainline = node.variations[0]
                move_list["items"].append(
                    build_move(mainline, move_list["items"]))

                for variation in node.variations[1:]:
                    if move_list["items"]:
                        line.append(move_list)
                    line.append(
                        new_list("variation", build_line(variation)))
                    move_list = new_list("move_list")

                node = mainline

            if move_list["items"]:
                line.append(move_list)

            return line

        return build_line(self.game)
