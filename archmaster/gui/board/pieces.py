from PySide6.QtSvg import QSvgRenderer

from archmaster.resources import resources


def load_piece(theme: str, symbol: str):
    color = ['w', 'b'][symbol.islower()]
    return QSvgRenderer(str(
        resources.pieces_dir / theme / f'{symbol.lower()}{color}.svg'))


class Pieces(dict):
    def __init__(self, theme):
        for symbol in 'PBNRQKpbnrqk':
            self[symbol] = load_piece(theme, symbol)
