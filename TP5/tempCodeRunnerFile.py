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