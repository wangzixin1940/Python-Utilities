from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from data.ui import zhCN
import qt_material as Stylesheet
import sys



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = zhCN.Ui_MainWindow()
        self.ui.setupUi(self)

def main():
    app = QApplication(sys.argv)
    Stylesheet.apply_stylesheet(app, "dark_medical.xml")
    window = MainWindow()
    window.setWindowIcon(QIcon("./images/pride.ico"))
    window.resize(320, 500)
    window.setFixedSize(320, 500)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
