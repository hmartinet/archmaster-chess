from PySide6 import QtCore, QtWidgets
from qt_material_icons import MaterialIcon


class ButtonGroupLayout(QtWidgets.QHBoxLayout):
    def __init__(self, parent=None, icon_size=24):
        super().__init__(parent)
        self.icon_size = icon_size

    def addButton(self, icon, tooltip, on_click, shortcut=None):
        btn = QtWidgets.QPushButton(MaterialIcon(
            icon, fill=True, size=self.icon_size), "")
        btn.setFlat(True)
        btn.setToolTip(tooltip)
        btn.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        btn.clicked.connect(on_click)
        if shortcut:
            btn.setShortcut(shortcut)
        self.addWidget(btn)
        return btn

    def addDropdownButton(self, icon, tooltip, indicator=True):
        btn = QtWidgets.QPushButton(MaterialIcon(icon, fill=True, size=24), "")
        btn.setFlat(True)
        if not indicator:
            btn.setStyleSheet(r"QPushButton::menu-indicator{width:0px;}")
        btn.setToolTip(tooltip)
        btn.setIconSize(QtCore.QSize(24, 24))
        self.addWidget(btn)
        return btn

    def addSpacer(self):
        self.addItem(QtWidgets.QSpacerItem(10, 0))

    def asWidget(self, noMargins=False):
        widget = QtWidgets.QWidget()
        if noMargins:
            self.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.addWidget(widget)
        self.setParent(widget)
        return widget

    def asFrame(self, shape: QtWidgets.QFrame.Shape = None, noMargins=False):
        frame = QtWidgets.QFrame()
        if shape:
            frame.setFrameShape(shape)
        if noMargins:
            self.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        frame.setLayout(self)
        self.setParent(frame)
        return frame
