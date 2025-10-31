from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QLineEdit, QVBoxLayout, \
    QHBoxLayout, QGridLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
import sys, os

from src.effects.graph import addres_to_node, node_to_coords
from src.effects.map import create_interactive_map, create_markers, create_route_in_map, outline_area
from src.logic.astar import a_star
from src.exceptions.validators import show_error_popup, validate_area_creation, \
    validate_route_calculation

app = QApplication(sys.argv)
win = QMainWindow()
place = None

def create_button(text, action):
    button = QPushButton(text)
    button.clicked.connect(action)
    return button

def not_loaded_map():
    label = QLabel("No hay área cargada")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("font-size: 18px; color: gray;")
    return label

def set_interactive_map():
    absolute_route = r"C:\Users\Danny\Documents\Trabajos UNA\Estructura de Datos\AppGPS\src\view\interactive_map.html"
    file_route = os.path.abspath(absolute_route)
    view = QWebEngineView()
    view.load(QUrl.fromLocalFile(file_route))
    return view

def load_interactive_map(selected_place=None, initial=False):
    if (not os.path.exists(r"C:\Users\Danny\Documents\Trabajos UNA\Estructura de Datos\AppGPS\src\view\interactive_map.html")
            and initial):
        return not_loaded_map()
    if selected_place is None or selected_place == "":
        return set_interactive_map()

    try:
        global place
        place = validate_area_creation(selected_place)
        m = create_interactive_map(place)
        outline_area(selected_place, m)
        return set_interactive_map()
    except Exception as e:
        show_error_popup(win, e)
        return set_interactive_map() #map without changes

def update_map_display(container_layout, new_content):
    while container_layout.count():
        child = container_layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

    container_layout.addWidget(new_content)


def create_route(origin, destination, calculate_distance):
    try:
        #validate
        validate_route_calculation(place, origin, destination)

        if calculate_distance:
            route, cost = a_star(place, addres_to_node(place, origin),
                           addres_to_node(place, destination), node_to_coords)
        else:
            route, cost = a_star(place, addres_to_node(place, origin),
                           addres_to_node(place, destination), node_to_coords, True)

        m = create_interactive_map(place)
        create_markers(origin, destination, m)
        create_route_in_map(place, m, route, cost)
        return set_interactive_map()

    except Exception as e:
        show_error_popup(win, e)
        return set_interactive_map() #map without changes

def window_settings(window):
    main_widget = create_UI()
    window.setCentralWidget(main_widget)
    window.setWindowTitle("GPS")
    window.resize(1200, 800)
    window.show()


def create_UI():
    # Labels
    lbl_selected_place = QLabel("Area:")
    lbl_origin = QLabel("Origen:")
    lbl_destination = QLabel("Destino:")

    # Field text
    txt_selected_place = QLineEdit()
    txt_origin = QLineEdit()
    txt_destination = QLineEdit()

    #container
    map_container = QWidget()
    map_layout = QVBoxLayout()
    map_container.setLayout(map_layout)

    initial_map = load_interactive_map(initial=True)
    map_layout.addWidget(initial_map)

    # Buttons - ahora actualizan el mapa display
    btn_load_area = create_button("Cargar Area",
                                  lambda: update_map_display(map_layout,
                                             load_interactive_map(txt_selected_place.text())))

    btn_less_distance = create_button("Menor Distancia",
                                      lambda: update_map_display(map_layout,
                                                create_route(txt_origin.text(), txt_destination.text(), calculate_distance=True)))

    btn_less_time = create_button("Menor Tiempo",
                                  lambda: update_map_display(map_layout,
                                             create_route(txt_origin.text(), txt_destination.text(), calculate_distance=False)))

    # Top panel
    pnl_top = QWidget()
    layout_top = QGridLayout()

    layout_top.addWidget(lbl_selected_place, 0, 0)
    layout_top.addWidget(txt_selected_place, 0, 1)

    layout_top.addWidget(lbl_origin, 1, 0)
    layout_top.addWidget(txt_origin, 1, 1)
    layout_top.addWidget(lbl_destination, 2, 0)
    layout_top.addWidget(txt_destination, 2, 1)

    # Buttons panel
    layout_buttons = QHBoxLayout()
    layout_buttons.addWidget(btn_less_distance)
    layout_buttons.addWidget(btn_less_time)
    layout_buttons.addWidget(btn_load_area)
    layout_buttons.addStretch()

    layout_top.addLayout(layout_buttons, 3, 0, 1, 3)
    pnl_top.setLayout(layout_top)

    #center
    pnl_center = QWidget()
    layout_central = QVBoxLayout()
    layout_central.addWidget(map_container)
    pnl_center.setLayout(layout_central)

    # Main panel
    main_widget = QWidget()
    main_layout = QVBoxLayout()

    main_layout.addWidget(pnl_top)  # top
    main_layout.addWidget(pnl_center)  # center

    # Size layouts
    main_layout.setStretchFactor(pnl_top, 1)
    main_layout.setStretchFactor(pnl_center, 4)

    main_widget.setLayout(main_layout)

    return main_widget

if __name__ == "__main__":
    window_settings(win)
    sys.exit(app.exec_())