import networkx as nx
import matplotlib.pyplot as plt

# Création du graphe
G = nx.DiGraph()

# Ajout des nœuds avec propriétés
G.add_node("Voler", propriétés={"locomotion"})
G.add_node("Oiseaux", propriétés=set())
G.add_node("Les Moineaux", propriétés=set())
G.add_node("Autruche", propriétés=set())

# Ajout des relations (y compris une exception)
relations = [
    ("Oiseaux", "Voler", "locomotion", False),
    ("Les Moineaux", "Oiseaux", "is-a", False),
    ("Autruche", "Oiseaux", "is-a", False),
    ("Autruche", "Voler", "locomotion", True)  # Lien d’exception
]

for src, dst, rel, is_exception in relations:
    G.add_edge(src, dst, relation=rel, exception=is_exception)

# === Algorithme d’héritage avec inhibition sur exception ===
def heritage_avec_inhibition(graph):
    def collect_props(node, visited=None):
        if visited is None:
            visited = set()
        if node in visited:
            return set()
        visited.add(node)

        props = set(graph.nodes[node]["propriétés"])

        for pred in graph.predecessors(node):
            edge = graph.edges[pred, node]
            if not edge.get("exception", False):
                rel = edge.get("relation")
                if rel in ["is-a", "locomotion"]:
                    props |= collect_props(pred, visited)
        return props

    for node in graph.nodes:
        graph.nodes[node]["propriétés"] = collect_props(node)

# Application de l’algorithme
heritage_avec_inhibition(G)

# Résultat final
for node, data in G.nodes(data=True):
    print(f"• {node} hérite : {data['propriétés']}")

# --- Affichage du graphe ---
pos = nx.spring_layout(G, seed=42)
edge_labels = nx.get_edge_attributes(G, 'relation')
exception_labels = nx.get_edge_attributes(G, 'exception')

# Crée des couleurs différentes pour les exceptions
edge_colors = ['red' if G.edges[edge].get('exception', False) else 'black' for edge in G.edges]

plt.figure(figsize=(10, 7))
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color=edge_colors, node_size=2000, font_size=10, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='green')

plt.title("Graphe d'héritage avec exceptions (rouge = exception)")
plt.show()
