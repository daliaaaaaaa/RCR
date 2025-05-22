import networkx as nx
import matplotlib.pyplot as plt

# Création du graphe orienté
G = nx.DiGraph()

# --- Ajout des noeuds avec marquage ---
nodes = {
    "Modes de Représentations des connaissances": "catégorie",
    "Modes Logiques": "catégorie",
    "Modes Graphiques": "catégorie",
    "Logiques Classiques": "catégorie",
    "Logiques Non classiques": "catégorie",
    "Logique D’ordre": "logique",
    "Logique D’ordre 0": "logique",
    "Axiome A4": "axiome",
    "Logique Modale": "logique",
    "Système T": "système",
    "Système D": "système",
    "Système S5": "système",
    "Axiome A7": "axiome",
    "a->a": "formule",
    "Logique Des défauts": "logique",
    "Logiques De description": "logique",
    "Réseaux Sémantique": "modèle",
    "Réseaux Bayésiens": "modèle",
    "Axel-IA": "acteur",
    "Reiter": "chercheur"
}

for node, ntype in nodes.items():
    G.add_node(node, type=ntype)

# --- Ajout des relations ---
edges = [
    ("Modes de Représentations des connaissances", "Modes Logiques", "is-a"),
    ("Modes de Représentations des connaissances", "Modes Graphiques", "is-a"),
    ("Modes Logiques", "Logiques Classiques", "is-a"),
    ("Modes Logiques", "Logiques Non classiques", "is-a"),
    ("Logiques Classiques", "Logique D’ordre", "is-a"),
    ("Logique D’ordre", "Axiome A4", "contient"),
    ("Logiques Classiques", "Logique D’ordre 0", "is-a"),
    ("Logiques Non classiques", "Logique Modale", "is-a"),
    ("Logique Modale", "Système T", "is-a"),
    ("Logique Modale", "Système D", "is-a"),
    ("Logique Modale", "Système S5", "is-a"),
    ("Système T", "Axiome A7", "contient"),
    ("Système D", "Axiome A7", "contient"),
    ("Axiome A7", "a->a", "is-a"),
    ("Logiques Non classiques", "Logique Des défauts", "is-a"),
    ("Logiques Non classiques", "Logiques De description", "is-a"),
    ("Modes Graphiques", "Réseaux Sémantique", "is-a"),
    ("Modes Graphiques", "Réseaux Bayésiens", "is-a"),
    ("Axel-IA", "Modes de Représentations des connaissances", "is-a"),
    ("Reiter", "Logique Des défauts", "a développé")
]

for src, dst, rel in edges:
    G.add_edge(src, dst, relation=rel)

# --- Affichage du graphe ---
pos = nx.spring_layout(G, seed=42)
edge_labels = nx.get_edge_attributes(G, 'relation')
node_labels = {node: f"{node}\n({data['type']})" for node, data in G.nodes(data=True)}

plt.figure(figsize=(18, 12))
nx.draw(G, pos, with_labels=True, labels=node_labels,
        node_color='lightblue', node_size=2000, font_size=8, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='black')
plt.title("Graphe sémantique - Modes de représentations des connaissances")
plt.axis('off')
plt.show()