import sys
from PyQt5.QtWidgets import QApplication
from src.view.window import Window_app

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gps_app = Window_app()
    gps_app.show()
    sys.exit(app.exec_())

#Para ejecutar la aplicación se debe abrir un cmd, luego
#ejecutar:
#cd "ruta\AppGPS" (según la ruta donde se haya guardado el proyecto)
#luego activar el entorno:
#env\Scripts\activate
#Por último ejecutar con:
#python app.py