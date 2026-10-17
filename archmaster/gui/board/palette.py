from PySide6 import QtGui


class Palette:
    _default = {
        'light': (.20, .90),
        'dark': (.30, .50),
        'board': 216,
        'move': (216 + 180) % 360,
        'badge::win': (134, .5, .5),
        'badge::lost': (0, .5, .5),
        'badge::draw': (60, .0, .25),
    }

    def __init__(self, name=None):
        self.config = self._default
        self.BOARD_LIGHT = self.get_color('board', 'light')
        self.BOARD_DARK = self.get_color('board', 'dark')
        self.MOVE_LIGHT = self.get_color('move', 'light', True)
        self.MOVE_DARK = self.get_color('move', 'dark', True)
        self.BADGE_WIN = self.get_badge_color('win')
        self.BADGE_LOST = self.get_badge_color('lost')
        self.BADGE_DRAW = self.get_badge_color('draw')

    def get_color(self, name, tone, limited=False):
        H = self.config[name]
        SL = self.config[tone]
        if limited:
            if tone == 'light':
                SL = max(SL[0], .8), min(SL[1], .8)
            if tone == 'dark':
                SL = max(SL[0], .8), max(SL[1], .4)
        return QtGui.QColor.fromHslF(H / 360., *SL)

    def get_badge_color(self, name):
        H, S, L = self.config[f"badge::{name}"]
        return QtGui.QColor.fromHslF(H / 360., S, L)
