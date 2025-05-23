import networkx as nx
import matplotlib.pyplot as plt

# =========================
# Données du graphe
# =========================
semantic_net = {
    "pomme": [("isa", "fruit")],
    "banane": [("isa", "fruit")],
    "carotte": [("isa", "légume")],
    "fruit": [("isa", "nourriture")],
    "légume": [("isa", "nourriture")]
}

properties = {
    "pomme": ["rouge"],
    "banane": ["jaune"],
    "carotte": ["orange"],
    "fruit": ["sucré"],
    "légume": ["sain"]
}

exceptions = {
    "carotte": ["sucré"]  # la carotte ne doit pas hériter de "sucré" même si "légume" hérite de "nourriture"
}

inheritance_links = {
    "pomme": "fruit",
    "banane": "fruit",
    "carotte": "légume",
    "fruit": "nourriture",
    "légume": "nourriture"
}

# =========================
# Fonctions
# =========================

def afficher_graphe(graphe, titre="Réseau sémantique", properties=None):
    G = nx.DiGraph()
    for noeud, liens in graphe.items():
        for relation, voisin in liens:
            G.add_edge(noeud, voisin, label=relation)
    if properties:
        for concept, props in properties.items():
            for prop in props:
                G.add_edge(concept, prop, label="a_propriété")

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')
    nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(titre)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def propagate_marker(graph, start_nodes, relation="isa"):
    visited = set()
    queue = list(start_nodes)
    result = set()

    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        result.add(node)

        for rel, target in graph.get(node, []):
            if rel == relation:
                queue.append(target)
    
    return result

def infer_properties(concept, inheritance_links, properties):
    inherited = set(properties.get(concept, []))
    current = concept
    while current in inheritance_links:
        parent = inheritance_links[current]
        inherited.update(properties.get(parent, []))
        current = parent
    return inherited

def infer_properties_with_exceptions(concept, inheritance_links, properties, exceptions):
    inherited = set(properties.get(concept, []))
    blocked = set(exceptions.get(concept, []))
    current = concept
    while current in inheritance_links:
        parent = inheritance_links[current]
        inherited.update(p for p in properties.get(parent, []) if p not in blocked)
        current = parent
    return inherited

# =========================
# Exécution / Tests
# =========================
if __name__ == "__main__":
    print("=== Propagation des marqueurs depuis 'pomme' et 'banane' ===")
    res1 = propagate_marker(semantic_net, ["pomme", "banane"])
    print("Résultat :", res1)

    print("\n=== Propriétés héritées par 'banane' ===")
    res2 = infer_properties("banane", inheritance_links, properties)
    print("Résultat :", res2)

    print("\n=== Propriétés héritées par 'carotte' avec exceptions ===")
    res3 = infer_properties_with_exceptions("carotte", inheritance_links, properties, exceptions)
    print("Résultat :", res3)

    afficher_graphe(semantic_net, "Réseau sémantique : Nourriture", properties=properties)
