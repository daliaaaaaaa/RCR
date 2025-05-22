# Code exact tel que transcrit du rapport TP5
# Note: Des fonctions avec le même nom sont redéfinies. Dans un script unique,
# la dernière définition sera celle utilisée si appelée par ce nom.

# Partie 1: implémenter l'algorithme de propagation de marqueurs dans les réseaux sémantiques
# Source: Figure 5.1

import json # Note: json import is shown in the figure context

def get_label(reseau_semantique, node, relation): # Définition 1 de get_label
    node_relation_edges = [edge["from"] for edge in reseau_semantique["edges"] if (edge["to"] == node["id"] and edge["label"] == relation)]
    node_relation_edges_label = [node["label"] for node in reseau_semantique["nodes"] if node["id"] in node_relation_edges]
    reponse = "il y a un lien entre les 2 noeuds: " + ", ".join(node_relation_edges_label)
    return reponse

def propagation_de_marqueurs(reseau_semantique, nodel, node2, relation): # Définition 1 de propagation_de_marqueurs
    nodes = reseau_semantique["nodes"]
    solutions_found = []

    for i in range(min(len(nodel), len(node2))):
        solution_found = False
        try:
            M1 = [node for node in nodes if node["label"] == nodel[i]][0]
            M2 = [node for node in nodes if node["label"] == node2[i]][0]
            edges = reseau_semantique["edges"]
            propagation_edges = [edge for edge in edges if (edge["to"] == M1["id"] and edge["label"] == "is a")]
            while len(propagation_edges) > 0 and not solution_found:
                temp_node = propagation_edges.pop()
                temp_node_contient_edges = [edge for edge in edges if (edge["from"] == temp_node["from"] and edge["label"] == relation)]
                solution_found = any(d['to'] == M2["id"] for d in temp_node_contient_edges)
                if not solution_found:
                    temp_node_is_a_edges = [edge for edge in edges if (edge["to"] == temp_node["from"] and edge["label"] == "is a")]
                    propagation_edges.extend(temp_node_is_a_edges)
            solutions_found.append(get_label(reseau_semantique, M2, relation) if solution_found else "il n'y a pas un lien entre les 2 noeuds") # Utilise get_label (Définition 1)
        except IndexError:
            solutions_found.append("Aucune reponse n'est fournie par manque de connaissances.")
    return(solutions_found)

# Partie 2: implémenter l'algorithme d'héritage
# Source: Figure 5.4

# import json # Déjà importé

def get_label(reseau_semantique, node_id): # Définition 2 de get_label (Redéfinition)
    node = next((node for node in reseau_semantique["nodes"] if node["id"] == node_id), None)
    if node:
        return node.get("label")
    else:
        return None

def heritage(reseau_semantique, name):
    the_end = False
    nodes = reseau_semantique["nodes"]
    edges = reseau_semantique["edges"]
    # Utilise get_label (Définition 2 car c'est la plus récente à ce point dans le script)
    node_obj = next((n for n in nodes if get_label(reseau_semantique, n["id"]) == name), None)
    if not node_obj: # Corrigé de 'node' à 'node_obj' pour correspondre à la variable définie
        print("Node with label '{}' not found.".format(name))
        return [], []
    node_id = node_obj["id"] # Corrigé de 'node["id"]' à 'node_obj["id"]'
    legacy_edges = [edge["to"] for edge in edges if (edge["from"] == node_id and edge["label"] == "is a ")] # Note the space in "is a "
    legacy = []
    properties = set()

    while not the_end:
        if not legacy_edges: # Ajout d'une vérification pour éviter pop sur liste vide
            the_end = True
            continue
        n = legacy_edges.pop(0)
        legacy.append(get_label(reseau_semantique, n)) # Utilise get_label (Définition 2)
        legacy_edges.extend([edge["to"] for edge in edges if (edge["from"] == n and edge["label"] == "is a ")]) # Note the space in "is a "
        
        # Le rapport indique "is a " pour la condition, mais pour les propriétés, on veut généralement "!="
        properties_nodes = [edge for edge in edges if (edge["from"] == n and edge["label"] != "is a ")]
        for pn in properties_nodes:
            if pn["label"] in ["vit dans", "a"]:
                properties.add(": ".join([pn["label"], get_label(reseau_semantique, pn["to"])])) # Utilise get_label (Définition 2)
        
        own_properties = [edge for edge in edges if (edge["from"] == node_id and edge["label"] != "is a ")]
        for op in own_properties:
            if op["label"] in ["vit dans", "a"]:
                properties.add(": ".join([op["label"], get_label(reseau_semantique, op["to"])])) # Utilise get_label (Définition 2)

        if not legacy_edges:
            the_end = True
            
    return legacy, list(properties)

# Ajout des relations (arcs)
G.add_edge("Mammifère", "Animal", relation="is-a")
G.add_edge("Mammifère", "vertèbres", relation="is-a")
G.add_edge("Ours", "Mammifère", relation="is-a")
G.add_edge("chat", "Mammifère", relation="is-a")
G.add_edge("chat", "Fourrure", relation="a")
G.add_edge("Ours", "Fourrure", relation="a")
G.add_edge("poisson", "Animal", relation="is-a")
G.add_edge("poisson", "eau", relation="vit dans")
G.add_edge("Baleine", "Mammifère", relation="is-a")
G.add_edge("Baleine", "eau", relation="vit dans")

# Affichage du graphe
pos = nx.spring_layout(G)
edge_labels = nx.get_edge_attributes(G, 'relation')
node_labels = {node: f"{node}\n({data['type']})" for node, data in G.nodes(data=True)}

nx.draw(G, pos, with_labels=True, labels=node_labels, node_color='lightblue', node_size=2500, font_size=9, font_weight='bold', arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
plt.title("Graphe sémantique - Exemple de marquage")
plt.axis('off')
plt.show()