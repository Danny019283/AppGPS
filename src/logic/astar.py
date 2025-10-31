from collections import namedtuple
from queue import PriorityQueue
import math as m

Node = namedtuple('Node', ['id', 'cost_from_origin', 'heuristic', 'function_cost', 'parent'])

def a_star(graph, origin, destination, node_to_coords, calculate_time = False):
    open_set = PriorityQueue()
    visited = set()

    h_start = haversine(node_to_coords(graph, origin), node_to_coords(graph, destination))
    start_node = Node(origin, 0, None, h_start, None)
    open_set.put((start_node.function_cost, start_node))

    while not open_set.empty():
        _, current = open_set.get()

        if current.id == destination:
            if calculate_time:
                cost = f"{round(current.cost_from_origin / 60)} minutos"
            else:
                c = str(current.cost_from_origin / 1000)
                cost = f"{c[:c.index('.') + 2] + " Km"}"
            return build_path(current), cost
        if current in visited:
            continue
        visited.add(current.id)

        if calculate_time:
            calculate_weight = route_in_less_time
        else:
            calculate_weight = route_in_less_distance

        for neighbor in graph.neighbors(current.id):
            if neighbor in visited:
                continue
            g_cost = calculate_weight(graph, current, neighbor)
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
    #get lat and lon from points of interes
    lat1, lon1 = origin
    lat2, lon2 = destination
    #to radians
    lat1,lon1 = m.radians(lat1), m.radians(lon1)
    lat2,lon2 = m.radians(lat2), m.radians(lon2)
    #earth radius in meters
    earth_radius = 6371000
    #calculate haversine for lat and lon
    hav_lat = m.sin((lat2 - lat1)/2)**2
    hav_lon = m.sin((lon2 - lon1)/2)**2
    return earth_radius * 2 * m.asin(m.sqrt(hav_lat + m.cos(lat1) * m.cos(lat2) * hav_lon))

def heuristic(graph, origin, destination):
    haversine((graph.nodes[origin]["y"], graph.nodes[origin]["x"]), destination)

def build_path(node):
    path = []
    while node:
        path.append(node.id)
        node = node.parent
    return list(reversed(path))

def route_in_less_distance(graph, current, neighbor):
    return current.cost_from_origin + graph[current.id][neighbor][0]["length"]

def route_in_less_time(graph, current, neighbor):
            distance = graph[current.id][neighbor][0]["length"]
            speed = get_speed(graph[current.id][neighbor][0])
            if speed:
                time = distance / (speed * 1000 / 3600)  # convert km/h to m/s
            else:
                # set mean speed if edge not specifies speed max
                highway_type = graph[current.id][neighbor][0].get("highway", "")
                mean_speed = {
                    "motorway": 100,
                    "trunk": 80,
                    "primary": 60,
                    "secondary": 50,
                    "tertiary": 40,
                    "residential": 30,
                    "service": 20
                }.get(highway_type, 40)
                time = distance / (mean_speed * 1000 / 3600)


            return current.cost_from_origin + time

def get_speed(edge_data):
    maxspeed = edge_data.get("maxspeed")
    if maxspeed is None:
        return None
    if isinstance(maxspeed, list):
        maxspeed = maxspeed[0]
    try:
        return float(str(maxspeed).split()[0]) #only number
    except:
        return None
