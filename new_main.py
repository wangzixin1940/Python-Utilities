from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QIcon
import zhCN
import sys



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = zhCN.Ui_MainWindow()
        self.ui.setupUi(self)

def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    window = MainWindow()
    window.setWindowIcon(QIcon("./images/pride.ico"))
    window.resize(320, 500)
    window.setFixedSize(320, 500)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
