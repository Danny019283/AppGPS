import folium
import osmnx as ox

def create_interactive_map(graph):
    nodes, edges = ox.graph_to_gdfs(graph)

    map = folium.Map(location=[nodes.y.mean(), nodes.x.mean()], zoom_start=13)

    # Guardar el mapa
    map.save("interactive_map.html")
    return map

def create_markers(origin, destination, map):
    ori_coords = ox.geocode(origin)
    dest_coords = ox.geocode(destination)

    folium.Marker(ori_coords, popup=f"Origen: {origin}", icon=folium.Icon(color="green")).add_to(map)
    folium.Marker(dest_coords, popup=f"Destino: {destination}", icon=folium.Icon(color="red")).add_to(map)
    map.save("interactive_map.html")

# Convertir la lista de nodos a coordenadas
def create_routes_in_map(graph, map, routes):
    coords = [(graph.nodes[n]['y'], graph.nodes[n]['x']) for n in routes]
    folium.PolyLine(
        coords,
        color="blue",
        weight=5,
        opacity=0.8,
        popup="Ruta"
    ).add_to(map)

    map.save("interactive_map.html")


    script = """
    <script>
      if (!sessionStorage.getItem("reloaded")) {
        sessionStorage.setItem("reloaded", "true");
        setTimeout(() => location.reload(), 2000);
      } else {
        sessionStorage.removeItem("reloaded");
      }
    </script>
    """

    with open("interactive_map.html", "r+", encoding="utf-8") as f:
        content = f.read()
        if script not in content:
            f.write(script)
