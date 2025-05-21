import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


# Création du graphe orienté
G = nx.DiGraph()

# --- Ajout des noeuds avec marquage ---
nodes = {
    "Modes de Représentations des connaissances": "catégorie",
    "Modes Logiques": "catégorie",
    "Modes Graphiques": "catégorie",
    "Logiques Classiques": "catégorie",
    "Logiques Non classiques": "catégorie",
    "Logique D’ordre 1": "logique",
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
    ("Logiques Classiques", "Logique D’ordre 1", "is-a"),
    ("Logique D’ordre 1", "Axiome A4", "contient"),
    ("Logiques Classiques", "Logique D'’'ordre 0", "is-a"),
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

# # --- Affichage du graphe ---
# pos = nx.spring_layout(G, seed=42)
# edge_labels = nx.get_edge_attributes(G, 'relation')
# node_labels = {node: f"{node}\n({data['type']})" for node, data in G.nodes(data=True)}

# plt.figure(figsize=(18, 12))
# nx.draw(G, pos, with_labels=True, labels=node_labels,
#         node_color='lightblue', node_size=2000, font_size=8, font_weight='bold')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='black')
# plt.title("Graphe sémantique - Modes de représentations des connaissances")
# plt.axis('off')
# plt.show()

# Fonction de propagation de marqueurs

def remonter_conteneurs(graph, cible, relation_filter=["contient", "is-a"]):
    visited = set()
    queue = deque([(cible, [cible])])
    chemins = []

    while queue:
        current_node, path = queue.popleft()
        visited.add(current_node)
        for predecessor in graph.predecessors(current_node):
            rel = graph.edges[predecessor, current_node].get("relation")
            if rel in relation_filter:
                new_path = [predecessor] + path
                chemins.append(new_path)
                if predecessor not in visited:
                    queue.append((predecessor, new_path))
    return chemins


# Supposons que G est déjà défini comme dans les exemples précédents
# quelles sont les modes de representations qui des connaissance qui contiennent l'axiome A7?
# Nœuds marqués
resultat = remonter_conteneurs(G, "Axiome A7", relation_filter=["contient", "is-a"])
# Affichage des résultats
racines = set([path[0] for path in resultat])  # concepts racines des chemins

print("Les modes de représentations des connaissances qui contiennent l’Axiome A7 sont :")
for concept in racines:
    print("•", concept)


# PARTIE II

# Ajouter des propriétés aux nœuds (comme attributs)
G.nodes["Système T"]["propriétés"] = {"P_T"}
G.nodes["Logique Modale"]["propriétés"] = {"P_Modale"}
G.nodes["Logiques Non classiques"]["propriétés"] = {"P_NC"}
G.nodes["Modes Logiques"]["propriétés"] = {"P_MLog"}
G.nodes["Modes de Représentations des connaissances"]["propriétés"] = {"P_MRC"}
G.nodes["Logiques Classiques"]["propriétés"] = {"P_LC"}

# Fonction pour propager les propriétés héritées
def heritage_et_saturation(graph):
    # Initialiser les propriétés héritées
    for node in graph.nodes:
        if "propriétés" not in graph.nodes[node]:
            graph.nodes[node]["propriétés"] = set()

    # Pour chaque nœud, propager les propriétés de ses ancêtres (via is-a)
    def collect_properties(node):
        props = set(graph.nodes[node]["propriétés"])
        for pred in graph.predecessors(node):
            rel = graph.edges[pred, node].get("relation")
            if rel == "is-a":
                props |= collect_properties(pred)
        return props

    # Saturer le graphe
    for node in graph.nodes:
        inherited = collect_properties(node)
        graph.nodes[node]["propriétés"] = inherited


# Appel de la fonction pour propager les propriétés
heritage_et_saturation(G)

print("Propriétés héritées par nœud :\n")
for node, data in G.nodes(data=True):
    if data["propriétés"]:
        print(f"{node} : {data['propriétés']}")



# Partie III
# pas de lien d'execption entre les noeuds
