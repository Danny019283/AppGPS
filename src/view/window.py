import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QPushButton,
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

from src.effects.graph import addres_to_node, node_to_coords
from src.effects.map import create_interactive_map, create_markers, create_route_in_map, outline_area
from src.logic.astar import a_star
from src.exceptions.validators import show_error_popup, validate_area_creation, validate_route_calculation
from src.logic.graph_representations import save_adjacency_list
from src.logic.pathfinding_algorithms import path_finding, bfs, dfs


class GPSApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.place = None
        self.selected_place = None

        self.txt_selected_place = QLineEdit()
        self.txt_origin = QLineEdit()
        self.txt_destination = QLineEdit()
        self.map_container = QWidget()
        self.map_layout = QVBoxLayout()
        self.web_view = None

        self.setWindowTitle("GPS")
        self.resize(1200, 800)

        # Setup UI
        self.setCentralWidget(self.create_UI())

    #Utility functions
    def create_button(self, text, action):
        button = QPushButton(text)
        button.clicked.connect(action)
        return button

    def not_loaded_map(self):
        label = QLabel("No hay área cargada")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; color: gray;")
        return label

    def set_interactive_map(self):
        absolute_route = r"C:\Users\Danny\Documents\Trabajos UNA\Estructura de Datos\AppGPS\src\view\interactive_map.html"
        file_route = os.path.abspath(absolute_route)
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl.fromLocalFile(file_route))
        return self.web_view

    def load_interactive_map(self, name_place=None, initial=False):
        try:
            if (not os.path.exists(r"C:\Users\Danny\Documents\Trabajos UNA\Estructura de Datos\AppGPS\src\view\interactive_map.html")
                    and initial):
                return self.not_loaded_map()
            if name_place is None or name_place == "":
                return self.set_interactive_map()

            self.selected_place = name_place
            self.place = validate_area_creation(name_place)
            m = create_interactive_map(self.place)
            outline_area(name_place, m)
            return self.set_interactive_map()
        except Exception as e:
            show_error_popup(self, e)
            return self.set_interactive_map()  # map without changes

    def update_map_display(self, new_content):
        while self.map_layout.count():
            child = self.map_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.map_layout.addWidget(new_content)

    def create_route(self, origin, destination, algorithm):
        try:
            validate_route_calculation(self.place, origin, destination)
            algorithms = {
                "astar distance": lambda: a_star(self.place, addres_to_node(self.place, origin),
                                                 addres_to_node(self.place, destination), node_to_coords),
                "astar time": lambda: a_star(self.place, addres_to_node(self.place, origin),
                                             addres_to_node(self.place, destination), node_to_coords, True),
                "bfs": lambda: (path_finding(self.place, origin, destination, bfs), None),
                "dfs": lambda: (path_finding(self.place, origin, destination, dfs), None)
            }
            route, cost = algorithms[algorithm]()
            m = create_interactive_map(self.place)
            outline_area(self.selected_place, m)
            create_markers(origin, destination, m)
            create_route_in_map(self.place, m, route, cost)
            return self.set_interactive_map()

        except Exception as e:
            show_error_popup(self, e)
            return self.set_interactive_map()

    def create_adjacency_list(self, graph):
        if graph is not None:
            save_adjacency_list(graph)

    #UI
    def create_UI(self):
        # Map container
        self.map_container.setLayout(self.map_layout)
        initial_map = self.load_interactive_map(initial=True)
        self.map_layout.addWidget(initial_map)

        # Labels
        lbl_selected_place = QLabel("Area:")
        lbl_origin = QLabel("Origen:")
        lbl_destination = QLabel("Destino:")

        # Buttons
        btn_load_area = self.create_button("Cargar Area",
                                           lambda: self.update_map_display(
                                               self.load_interactive_map(self.txt_selected_place.text())
                                           ))

        btn_less_distance = self.create_button("Menor Distancia",
                                              lambda: self.update_map_display(
                                                  self.create_route(self.txt_origin.text(),
                                                                    self.txt_destination.text(),
                                                                    "astar distance")
                                              ))

        btn_less_time = self.create_button("Menor Tiempo",
                                          lambda: self.update_map_display(
                                              self.create_route(self.txt_origin.text(),
                                                                self.txt_destination.text(),
                                                                "astar time")
                                          ))

        btn_bfs = self.create_button("BFS",
                                     lambda: self.update_map_display(
                                         self.create_route(self.txt_origin.text(),
                                                           self.txt_destination.text(),
                                                           "bfs")
                                     ))

        btn_dfs = self.create_button("DFS",
                                     lambda: self.update_map_display(
                                         self.create_route(self.txt_origin.text(),
                                                           self.txt_destination.text(),
                                                           "dfs")
                                     ))

        btn_adjacency_list = self.create_button("Lista de Adyacencias",
                                                lambda: self.create_adjacency_list(self.place))

        # Top panel
        pnl_top = QWidget()
        layout_top = QGridLayout()
        layout_top.addWidget(lbl_selected_place, 0, 0)
        layout_top.addWidget(self.txt_selected_place, 0, 1)
        layout_top.addWidget(lbl_origin, 1, 0)
        layout_top.addWidget(self.txt_origin, 1, 1)
        layout_top.addWidget(lbl_destination, 2, 0)
        layout_top.addWidget(self.txt_destination, 2, 1)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(btn_less_distance)
        layout_buttons.addWidget(btn_less_time)
        layout_buttons.addWidget(btn_load_area)
        layout_buttons.addWidget(btn_bfs)
        layout_buttons.addWidget(btn_dfs)
        layout_buttons.addWidget(btn_adjacency_list)
        layout_buttons.addStretch()

        layout_top.addLayout(layout_buttons, 3, 0, 1, 3)
        pnl_top.setLayout(layout_top)

        # Center panel
        pnl_center = QWidget()
        layout_central = QVBoxLayout()
        layout_central.addWidget(self.map_container)
        pnl_center.setLayout(layout_central)

        # Main panel
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(pnl_top)
        main_layout.addWidget(pnl_center)
        main_layout.setStretchFactor(pnl_top, 1)
        main_layout.setStretchFactor(pnl_center, 4)
        main_widget.setLayout(main_layout)

        return main_widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gps_app = GPSApp()
    gps_app.show()
    sys.exit(app.exec_())
