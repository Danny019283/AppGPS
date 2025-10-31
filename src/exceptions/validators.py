from PyQt5.QtWidgets import QMessageBox
import osmnx as ox
from src.exceptions.gps_exceptions import *


def validate_route_calculation(place, origin, destination):
    validate_fields(("Origen", origin), ("Destino", destination))

    validate_area_loaded(place)

    origin_coords = validate_address_exists(origin, "origen")
    destination_coords = validate_address_exists(destination, "destino")

    validate_point_in_area(place, origin_coords, "origen")
    validate_point_in_area(place, destination_coords, "destino")

    return origin_coords, destination_coords


def validate_address_exists(address, point_name):
    try:
        return ox.geocode(address)
    except Exception:
        raise AddressNotFoundError(f"{point_name} ({address})")


def validate_point_in_area(graph, point_coords, point_name, tolerance=0.1):
    if graph is None:
        return False

    try:
        # Obtener bounds del grafo
        nodes = [graph.nodes[node] for node in graph.nodes()]
        lats = [node['y'] for node in nodes]
        lons = [node['x'] for node in nodes]

        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)

        point_lat, point_lon = point_coords

        # Verificar con tolerancia
        in_area = (min_lat - tolerance <= point_lat <= max_lat + tolerance and
                   min_lon - tolerance <= point_lon <= max_lon + tolerance)

        if not in_area:
            raise PointOutsideAreaError(point_name, "specified area")
        return None

    except Exception as e:
        # if jump an error, it is assumed that is not in specified area
        raise PointOutsideAreaError(point_name, "specified area")


def validate_area_creation(place_name):
    if not place_name or not place_name.strip():
        raise EmptyFieldError("Área")

    try:
        place = ox.graph_from_place(place_name, network_type="drive", simplify=False)
        return place
    except Exception as e:
        raise RouteCalculationError(f"No se pudo cargar el área '{place_name}': {str(e)}")


def validate_fields(*fields):
    for field_name, field_value in fields:
        if not field_value or not field_value.strip():
            raise EmptyFieldError(field_name)


def validate_area_loaded(place):
    if place is None:
        raise AreaNotLoadedError()


def show_error_popup(parent, exception):
    """Muestra un popup de error genérico"""
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText(str(exception))
    msg.exec_()