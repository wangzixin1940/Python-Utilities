from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
import qfluentwidgets
import sys

def main():
    app = QApplication(sys.argv)
    ui_file = QFile("./data/ui/zh-cn.ui")
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open UI file: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
