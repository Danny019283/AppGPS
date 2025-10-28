import time
import osmnx as ox

def create_graph_from_osm(selected_p):
    graph = None
    for attempt in range(3):
        try:
            print("Obteniendo datos de OSM...")
            graph = ox.graph_from_place(selected_p, network_type="drive", simplify=False)
            print("Descarga completada correctamente.")
            break
        except Exception as e:
            print(f"Intento {attempt+1} falló: {e}")
            time.sleep(5)
    return graph

def addres_to_node(graph, address):
    lat, lon = ox.geocode(address)
    return ox.distance.nearest_nodes(graph, lon, lat)

def node_to_coords(graph, node):
    return graph.nodes[node]['y'], graph.nodes[node]['x']

