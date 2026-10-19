from PySide6 import QtCore


class Progress(QtCore.QObject):
    value_changed = QtCore.Signal()

    def __init__(self, step_weights):
        super().__init__()
        self.step_weights = step_weights
        self.value = .0
        self.step = 0
        self.label = ""

    def next_step(self, label):
        self.value = sum(self.step_weights[:self.step])
        self.step += 1
        self.label = label
        self.value_changed.emit()

    def update_value(self, step_value):
        old_percent = int(self.value * 100)
        self.value = (
            sum(self.step_weights[:self.step - 1]) +
            step_value * self.step_weights[self.step - 1])
        new_percent = int(self.value * 100)
        if new_percent != old_percent:
            self.value_changed.emit()
