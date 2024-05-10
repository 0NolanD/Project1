import sys
from PyQt6 import QtWidgets
from gui import Ui_MainWindow
from logic import GradingLogic

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    logic = GradingLogic(ui)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()