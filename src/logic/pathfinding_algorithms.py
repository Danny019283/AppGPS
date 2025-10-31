from collections import deque
import osmnx as ox
from src.effects.graph import address_to_coords

def path_finding(graph, origin, destination, algorithm):
    lon_ori, lat_ori = address_to_coords(origin)
    lon_dest, lat_dest = address_to_coords(destination)
    origin = ox.distance.nearest_nodes(graph, lon_ori, lat_ori)
    destination = ox.distance.nearest_nodes(graph, lon_dest, lat_dest)
    return algorithm(graph, origin, destination)

def bfs(graph, origin, destination):
    visited = set()
    queue = deque([origin])
    parent = {}

    while queue:
        node = queue.popleft()
        if node == destination:
            return reconstruct_path(parent, origin, destination)
        if node not in visited:
            visited.add(node)
            for neighbor in list(graph.neighbors(node)):
                if neighbor not in visited:
                    queue.append(neighbor)
                    parent[neighbor] = node
    return None

def dfs(graph, origin, destination):
    visited = set()
    stack = [origin]
    parent = {}
    while stack:
        node = stack.pop()
        if node == destination:
            return reconstruct_path(parent, origin, destination)
        if node not in visited:
            visited.add(node)
            for neighbor in list(graph.neighbors(node)):
                if neighbor not in visited:
                    stack.append(neighbor)
                    parent[neighbor] = node
    return None

def reconstruct_path(parent, origin, destination):
    path = []
    current = destination
    while current != origin:
        path.append(current)
        current = parent.get(current)
        if current is None:
            return None
    path.append(origin)
    path.reverse()
    return path