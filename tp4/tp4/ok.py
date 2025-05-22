import json

def get_label(reseau_semantique, node, relation):
    node_relation_edges = [edge["from"] for edge in reseau_semantique["edges"] if (edge["to"] == node["id"] and edge["label"] == relation)]
    node_relation_edges_label = [node["label"] for node in reseau_semantique["nodes"] if node["id"] in node_relation_edges]
    reponse = "il y a un lion entre les 2 noeuds : " + " ".join(node_relation_edges_label)
    return reponse

def propagation_de_marqueurs(reseau_semantique, node1, node2, relation):
    nodes = reseau_semantique["nodes"]
    # solutions_found = []  # This line seems to be commented out or incomplete in the image

    solutions_found = []

    for i in range(min(len(node1), len(node2))):
        solution_found = False

        try:
            M1 = [node for node in nodes if node["label"] == node1[i][0]]
            M2 = [node for node in nodes if node["label"] == node2[i][0]]

            edges = reseau_semantique["edges"]
            propagation_edges = [edge for edge in edges if (edge["to"] == M1["id"] and edge["label"] == "is a")] # Potential issue: M1 is a list
            while len(propagation_edges) != 0 and not solution_found:
                temp_node = propagation_edges.pop()
                temp_node_content_edges = [edge for edge in edges if (edge["from"] == temp_node["from"] and edge["label"] == relation)] # Potential issue: temp_node structure
                solution_found = any(d["to"] == M2["id"] for d in temp_node_content_edges) # Potential issue: M2 is a list
                if not solution_found:
                    temp_node_is_a_edges = [edge for edge in edges if (edge["to"] == temp_node["from"] and edge["label"] == "is a")] # Potential issue: temp_node structure
                    propagation_edges.extend(temp_node_is_a_edges)

            solutions_found.append(get_label(reseau_semantique, M2, relation) if solution_found else "il n'y a pas un lien entre les 2 noeuds") # Potential issue: M2 is a list

        except IndexError:
            solutions_found.append("Aucune reponse n'est fournie par manque de connaissances.") # Apostrophe might be an issue if not handled as string literal

    return solutions_found