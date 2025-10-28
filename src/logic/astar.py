from collections import namedtuple
from queue import PriorityQueue
import math as m

Node = namedtuple('Node', ['id', 'cost_from_origin', 'heuristic', 'function_cost', 'parent'])

def a_star(graph, origin, destination, node_to_coords):
    open_set = PriorityQueue()
    visited = set()

    h_start = haversine(node_to_coords(graph, origin), node_to_coords(graph, destination))
    start_node = Node(origin, 0, None, h_start, None)
    open_set.put((start_node.function_cost, start_node))

    while not open_set.empty():
        _, current = open_set.get()

        if current.id == destination:
            distance = str(current.cost_from_origin/1000)
            print(distance[:distance.index('.') + 2] + "Km")
            return build_path(current)
        if current in visited:
            continue
        visited.add(current.id)

        for neighbor in graph.neighbors(current.id):
            if neighbor in visited:
                continue
            g_cost = current.cost_from_origin + graph[current.id][neighbor][0]["length"]  # peso real
            h = haversine(node_to_coords(graph, neighbor), node_to_coords(graph, destination))
            f_cost = g_cost + h

            # Crear nuevo nodo
            neighbor_node = Node(
                id = neighbor,
                cost_from_origin = g_cost,
                heuristic = h,
                function_cost =  f_cost,
                parent = current
            )

            open_set.put((neighbor_node.function_cost, neighbor_node))
    return None

def haversine(origin, destination):
    #obtenemos la latitud y longitud de los puntos deseados
    lat1, lon1 = origin
    lat2, lon2 = destination
    #pasamos a radianes
    lat1,lon1 = m.radians(lat1), m.radians(lon1)
    lat2,lon2 = m.radians(lat2), m.radians(lon2)
    #radio de la tierra en metros
    earth_radius = 6371000
    #calcular haverside a lat y lon
    hav_lat = m.sin((lat2 - lat1)/2)**2
    hav_lon = m.sin((lon2 - lon1)/2)**2
    #se calcula la ley haverside
    return earth_radius * 2 * m.asin(m.sqrt(hav_lat + m.cos(lat1) * m.cos(lat2) * hav_lon))

def heuristic(graph, origin, destination):
    haversine((graph.nodes[origin]["y"], graph.nodes[origin]["x"]), destination)

def build_path(node):
    path = []
    while node:
        path.append(node.id)
        node = node.parent
    return list(reversed(path))