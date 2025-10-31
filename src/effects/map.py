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
def create_route_in_map(graph, map, route, cost):
    coords = [(graph.nodes[n]['y'], graph.nodes[n]['x']) for n in route]

    popup_html = f"""
    <div style="text-align: center; font-family: Arial, sans-serif; min-width: 200px;">
        <h4 style="margin: 5px 0; color: #2c3e50; font-size: 16px;">📊 INFORMACIÓN DE RUTA</h4>
        <hr style="margin: 8px 0; border: 1px solid #bdc3c7;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; margin: 12px 0; color: white;">
            <p style="font-size: 20px; font-weight: bold; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                {cost}
            </p>
        </div>
    </div>"""
    folium.PolyLine(
        coords,
        color="blue",
        weight=5,
        opacity=0.8,
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(map)

    map.save("interactive_map.html")

def outline_area(place_name,map):
    area = ox.geocode_to_gdf(place_name)
    folium.GeoJson(
        area,
        style_function=lambda x: {
            'fillColor': 'red',
            'color': 'red',
            'weight': 3,
            'fillOpacity': 0
        }
    ).add_to(map)
    map.save("interactive_map.html")