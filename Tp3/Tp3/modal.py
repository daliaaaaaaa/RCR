import networkx as nx
import matplotlib.pyplot as plt

# --- Partie 1: Définition des Formules Modales (avec __repr__ ASCII) ---
class Propos:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return isinstance(other, Propos) and self.name == other.name
    def __hash__(self):
        return hash(self.name)

class Non:
    def __init__(self, formule):
        self.formule = formule
    def __repr__(self):
        return f"~{self.formule}" # ASCII

class Et:
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2
    def __repr__(self):
        return f"({self.f1} & {self.f2})" # ASCII

class Ou:
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2
    def __repr__(self):
        return f"({self.f1} | {self.f2})" # ASCII

class Implique: # Représente ⊃
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2
    def __repr__(self):
        return f"({self.f1} >> {self.f2})" # ASCII

class Necessaire: # Carré (Box) - Représente □
    def __init__(self, formule):
        self.formule = formule
    def __repr__(self):
        return f"Box({self.formule})" # ASCII (ou "[]")

class Possible: # Losange (Diamond) - Représente ◇
    def __init__(self, formule):
        self.formule = formule
    def __repr__(self):
        return f"Dia({self.formule})" # ASCII (ou "<>")

# --- Partie 2: Définition du Modèle de Kripke ---
class ModeleKripke:
    def __init__(self, nom_modele="Mon Modèle"):
        self.nom = nom_modele
        self.mondes = set()
        self.relation_R = {}
        self.valuation_V = {}

    def ajouter_monde(self, nom_monde):
        if nom_monde not in self.mondes:
            self.mondes.add(nom_monde)
            self.relation_R[nom_monde] = set()
            self.valuation_V[nom_monde] = set()

    def ajouter_mondes(self, liste_noms_mondes):
        for nom_monde in liste_noms_mondes:
            self.ajouter_monde(nom_monde)

    def ajouter_relation(self, monde_origine, monde_destination):
        if monde_origine not in self.mondes: self.ajouter_monde(monde_origine)
        if monde_destination not in self.mondes: self.ajouter_monde(monde_destination)
        self.relation_R[monde_origine].add(monde_destination)

    def ajouter_proposition_vraie(self, monde, nom_proposition_str):
        if monde not in self.mondes: self.ajouter_monde(monde)
        self.valuation_V[monde].add(nom_proposition_str)

    def mondes_accessibles(self, monde):
        return self.relation_R.get(monde, set())

    def est_vraie_prop(self, monde, nom_proposition_str):
        return nom_proposition_str in self.valuation_V.get(monde, set())

    def __repr__(self):
        representation = f"Modèle de Kripke: {self.nom}\n"
        representation += "------------------------------\n"
        representation += f"Mondes (W): {sorted(list(self.mondes))}\n"
        representation += "Relation d'Accessibilité (R):\n"
        for monde_key in sorted(list(self.relation_R.keys())):
            accessibles = self.relation_R[monde_key]
            if accessibles: representation += f"  {monde_key} -> {sorted(list(accessibles))}\n"
        representation += "Valuation (V) - Propositions vraies:\n"
        for monde_key in sorted(list(self.valuation_V.keys())):
            props_vraies = self.valuation_V[monde_key]
            if props_vraies: representation += f"  Dans {monde_key}: {sorted(list(props_vraies))}\n"
        if not any(self.valuation_V.values()): representation += "  (Aucune proposition n'est vraie)\n"
        representation += "------------------------------"
        return representation

# --- Partie 3: Fonction d'Évaluation des Formules ---
def evaluer(formule, modele: ModeleKripke, monde_actuel: str) -> bool:
    if monde_actuel not in modele.mondes:
        raise ValueError(f"Monde '{monde_actuel}' non trouvé dans le modèle pour l'évaluation.")

    if isinstance(formule, Propos):
        return modele.est_vraie_prop(monde_actuel, formule.name)
    elif isinstance(formule, Non):
        return not evaluer(formule.formule, modele, monde_actuel)
    elif isinstance(formule, Et):
        return evaluer(formule.f1, modele, monde_actuel) and evaluer(formule.f2, modele, monde_actuel)
    elif isinstance(formule, Ou):
        return evaluer(formule.f1, modele, monde_actuel) or evaluer(formule.f2, modele, monde_actuel)
    elif isinstance(formule, Implique):
        return (not evaluer(formule.f1, modele, monde_actuel)) or evaluer(formule.f2, modele, monde_actuel)
    elif isinstance(formule, Necessaire):
        mondes_a_verifier = modele.mondes_accessibles(monde_actuel)
        if not mondes_a_verifier: return True # □φ est vrai si pas de successeurs
        for monde_accessible in mondes_a_verifier:
            if not evaluer(formule.formule, modele, monde_accessible): return False
        return True
    elif isinstance(formule, Possible):
        mondes_a_verifier = modele.mondes_accessibles(monde_actuel)
        if not mondes_a_verifier: return False # ◇φ est faux si pas de successeurs
        for monde_accessible in mondes_a_verifier:
            if evaluer(formule.formule, modele, monde_accessible): return True
        return False
    else:
        raise TypeError(f"Type de formule non supporté: {type(formule)}")

# --- Partie 5: Visualisation (Optionnelle) ---
# MODIFIÉE pour ne pas utiliser Graphviz
def visualiser_modele_kripke(modele_kripke, titre_suffix=""):
    # Vérifie si les modules ont été importés avec succès (au cas où ils seraient chargés conditionnellement)
    # Pour ce script, ils sont importés globalement en haut.
    global nx, plt 
    if 'nx' not in globals() or 'plt' not in globals():
         print("\nLes bibliothèques networkx et matplotlib sont nécessaires pour la visualisation.")
         print("Assurez-vous qu'elles sont importées au début du script.")
         print("Vous pouvez les installer avec : pip install networkx matplotlib")
         return
    
    G = nx.DiGraph()
    for monde_visu in modele_kripke.mondes:
        props_vraies_str = ", ".join(sorted(list(modele_kripke.valuation_V.get(monde_visu, set()))))
        label = f"{monde_visu}\n({props_vraies_str})" if props_vraies_str else monde_visu
        G.add_node(monde_visu, label=label)

    for origine, destinations in modele_kripke.relation_R.items():
        for dest in destinations:
            G.add_edge(origine, dest)

    plt.figure(figsize=(12, 8))
    
    print("\nUtilisation de 'spring_layout' de NetworkX pour la visualisation (pas de dépendance Graphviz).")
    # D'autres dispositions NetworkX sans dépendances externes que vous pourriez essayer :
    # pos = nx.circular_layout(G)
    # pos = nx.kamada_kawai_layout(G) # Peut donner de bons résultats pour les graphes de taille moyenne
    # pos = nx.shell_layout(G)
    # pos = nx.spectral_layout(G)
    # pos = nx.random_layout(G, seed=42)
    
    # Utilisation de spring_layout
    # Vous pouvez ajuster les paramètres k et iterations pour changer l'apparence.
    # seed=42 assure que la disposition est la même à chaque exécution.
    pos = nx.spring_layout(G, k=1.5, iterations=70, seed=42) 
    
    labels_nodes = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, with_labels=False, node_size=4000, node_color="skyblue",
            font_size=9, arrows=True, arrowstyle='-|>', arrowsize=20,
            edge_color='gray', width=1.5)
    nx.draw_networkx_labels(G, pos, labels=labels_nodes, font_size=10, font_weight='bold')
    
    plt.title(f"Visualisation du Modèle de Kripke: {modele_kripke.nom}{titre_suffix}", fontsize=16)
    plt.show()

# --- Partie 4: Application à l'Exercice 2 ---
if __name__ == "__main__":
    # 1. Définir les propositions de l'exercice
    prop_a = Propos("a")
    prop_b = Propos("b")
    prop_c = Propos("c")
    prop_d = Propos("d")

    # 2. Créer le modèle de Kripke M de l'exercice
    modele_M = ModeleKripke("Modèle de l'Exercice 2")

    # Ajouter les mondes W = {w1, w2, w3, w4, w5, w6}
    modele_M.ajouter_mondes(['w1', 'w2', 'w3', 'w4', 'w5', 'w6'])

    # Définir la relation d'accessibilité R
    relations_R = [
        ('w1', 'w2'), ('w1', 'w3'),
        ('w3', 'w3'), ('w3', 'w4'), ('w3', 'w5'), ('w3', 'w6'),
        ('w4', 'w4'), ('w4', 'w5'),
        ('w6', 'w5')
    ]
    for orig, dest in relations_R:
        modele_M.ajouter_relation(orig, dest)

    # Définir la valuation V
    modele_M.ajouter_proposition_vraie('w1', 'a')
    modele_M.ajouter_proposition_vraie('w1', 'c')
    modele_M.ajouter_proposition_vraie('w2', 'b')
    modele_M.ajouter_proposition_vraie('w3', 'a')
    modele_M.ajouter_proposition_vraie('w4', 'b')
    modele_M.ajouter_proposition_vraie('w4', 'd')
    modele_M.ajouter_proposition_vraie('w5', 'c')
    modele_M.ajouter_proposition_vraie('w6', 'a')
    modele_M.ajouter_proposition_vraie('w6', 'b')
    modele_M.ajouter_proposition_vraie('w6', 'd')

    print("Description du Modèle de Kripke M (Exercice 2):")
    print(modele_M)
    print("\n")

    print("Évaluation des Formules de l'Exercice 2:")
    print("---------------------------------------")
    
    # Formules de l'exercice
    # a) M, w1 |= □(◇a ∨ ¬b)
    formule_2a = Necessaire(Ou(Possible(prop_a), Non(prop_b)))
    monde_2a = 'w1'
    resultat_2a = evaluer(formule_2a, modele_M, monde_2a)
    print(f"a) M, {monde_2a} |= {formule_2a}   :   {resultat_2a}")

    # b) M, w2 |= ¬(◇((c ⊃ ¬b) ∨ ◇a))
    formule_2b = Non(Possible(Ou(Implique(prop_c, Non(prop_b)), Possible(prop_a))))
    monde_2b = 'w2'
    resultat_2b = evaluer(formule_2b, modele_M, monde_2b)
    print(f"b) M, {monde_2b} |= {formule_2b}   :   {resultat_2b}")

    # c) M, w3 |= ◇(a ∧ ¬c) 
    formule_2c = Possible(Et(prop_a, Non(prop_c))) 
    monde_2c = 'w3'
    resultat_2c = evaluer(formule_2c, modele_M, monde_2c)
    print(f"c) M, {monde_2c} |= {formule_2c}   :   {resultat_2c}")

    # d) M, w4 |= □(c ∨ d)
    formule_2d = Necessaire(Ou(prop_c, prop_d))
    monde_2d = 'w4'
    resultat_2d = evaluer(formule_2d, modele_M, monde_2d)
    print(f"d) M, {monde_2d} |= {formule_2d}   :   {resultat_2d}")

    # e) M, w5 |= ◇( (□(a ∧ c)) ∧ d ) -- Version de votre code original
    formule_2e = Possible(Et(Necessaire(Et(prop_a, prop_c)), prop_d))
    monde_2e = 'w5'
    resultat_2e = evaluer(formule_2e, modele_M, monde_2e)
    print(f"e) M, {monde_2e} |= {formule_2e}   :   {resultat_2e}")
    
    # f) M, w6 |= ¬(□(□((¬c) ∨ (¬b))))
    formule_2f = Non(Necessaire(Necessaire(Ou(Non(prop_c), Non(prop_b)))))
    monde_2f = 'w6'
    resultat_2f = evaluer(formule_2f, modele_M, monde_2f)
    print(f"f) M, {monde_2f} |= {formule_2f}   :   {resultat_2f}")


    print("\nTentative de visualisation du modèle de l'exercice...")
    # La visualisation utilisera spring_layout par défaut
    visualiser_modele_kripke(modele_M)