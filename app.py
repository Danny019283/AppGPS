import sys
from PyQt5.QtWidgets import QApplication
from src.view.window import Window_app

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gps_app = Window_app()
    gps_app.show()
    sys.exit(app.exec_())