import networkx as nx
import osmnx as ox


def write_to_file(file_name, line, mode = "a"):
    with open(file_name, mode, encoding="utf-8") as file:
        file.write(line + "\n")


def save_adjacency_list(graph, file_name: str = "adyacent_list.txt"):
    write_to_file(file_name, "", mode="w")
    mapping = {node: i for i, node in enumerate(graph.nodes())}
    G = nx.relabel_nodes(graph, mapping)

    for node in G.nodes():
        neighbors = []
        for neighbor in G.neighbors(node):
            for key in G[node][neighbor]:
                weight = G[node][neighbor][key].get("length", 0)
                neighbors.append(f"({neighbor}, {weight:.2f} metros)")

        line = f"{node}: " + ", ".join(neighbors)
        write_to_file(file_name, line)

def adyacent_matrix():
    return