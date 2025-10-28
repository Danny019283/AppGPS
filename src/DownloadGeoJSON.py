import osmnx as ox
import time

ox.settings.timeout = 180
ox.settings.overpass_endpoint = "https://overpass-api.de/api/interpreter"

G = None
for attempt in range(3):
    try:
        print(f"Descargando datos... intento {attempt+1}")
        G = ox.graph_from_place("Provincia de Alajuela, Costa Rica", network_type="drive")
        print("✅ Descarga completada correctamente.")
        break
    except Exception as e:
        print(f"❌ Intento {attempt+1} falló: {e}")
        time.sleep(5)

if G is not None:
    nodos, aristas = ox.graph_to_gdfs(G)
    aristas.to_file("alajuela_aristas.geojson", driver="GeoJSON")
    nodos.to_file("alajuela_nodos.geojson", driver="GeoJSON")
    print("💾 Archivo guardado: alajuela.geojson")
else:
    print("⚠️ No se pudo descargar el mapa después de varios intentos.")
