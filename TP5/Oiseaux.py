import networkx as nx

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
