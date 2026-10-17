import os
import sys

from PySide6.QtWidgets import QApplication

from archmaster.gui.main_window import MainWindow

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"


def main():
    app = QApplication(sys.argv)
    app.setStyle("Material")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
