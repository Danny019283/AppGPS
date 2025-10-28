import osmnx as ox

from src.effects.graph import create_graph_from_osm, addres_to_node, node_to_coords
from src.effects.map import create_interactive_map, create_markers, create_routes_in_map
from src.logic.astar import a_star

#app
def app():
    selected_place =  "Naranjo, Alajuela, Costa Rica"
    place = create_graph_from_osm(selected_place)

    origin_address = "Escuela El Rosario, Calle Rosario, Guapinol, Santa Margarita, El Rosario, Naranjo, Alajuela, 20607, Costa Rica"
    destination_address = "Ebais El Rosario, Calle Rosario, Guapinol, Santa Margarita, El Rosario, Naranjo, Alajuela, 20607, Costa Rica"


    routes = a_star(place, addres_to_node(place, origin_address), addres_to_node(place, destination_address), node_to_coords)
    print(routes)

    m = create_interactive_map(place)
    create_markers(origin_address, destination_address, m)
    create_routes_in_map(place, m, routes)

if __name__ == "__main__":
    app()