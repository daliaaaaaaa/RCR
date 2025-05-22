import networkx as nx
import matplotlib.pyplot as plt

# --- Partie 1: Définition des Formules Modales (avec __repr__ ASCII) ---
class Propos:
    """
    Représente une proposition atomique dans la logique modale (ex: 'p', 'q', 'a', 'b').
    """
    def __init__(self, name):
        """
        Initialise une proposition avec son nom.
        :param name: Le nom de la proposition (chaîne de caractères).
        """
        self.name = name

    def __repr__(self):
        """
        Fournit une représentation textuelle de la proposition pour l'affichage.
        """
        return self.name

    def __eq__(self, other):
        """
        Définit l'égalité entre deux objets Propos, basée sur leur nom.
        """
        return isinstance(other, Propos) and self.name == other.name

    def __hash__(self):
        """
        Définit la fonction de hachage pour permettre l'utilisation des objets Propos 
        dans des sets ou comme clés de dictionnaires.
        """
        return hash(self.name)

class Non:
    """
    Représente symboles la négation logique (~ ou ¬).
    """
    def __init__(self, formule):
        """
        Initialise une négation avec la formule qu'elle nie.
        :param formule: L'objet formule (Propos, Et, Ou, etc.) à nier.
        """
        self.formule = formule

    def __repr__(self):
        """
        Fournit une représentation textuelle de la négation (ex: ~p).
        """
        return f"~{self.formule}" # Utilisation du tilde ASCII pour "Non"

class Et:
    """
    Représente la conjonction logique (& ou ∧).
    """
    def __init__(self, f1, f2):
        """
        Initialise une conjonction avec les deux formules qu'elle connecte.
        :param f1: La première formule.
        :param f2: La deuxième formule.
        """
        self.f1 = f1
        self.f2 = f2

    def __repr__(self):
        """
        Fournit une représentation textuelle de la conjonction (ex: (p & q)).
        """
        return f"({self.f1} & {self.f2})" # Utilisation de l'esperluette ASCII pour "Et"

class Ou:
    """
    Représente la disjonction logique (| ou ∨).
    """
    def __init__(self, f1, f2):
        """
        Initialise une disjonction avec les deux formules qu'elle connecte.
        :param f1: La première formule.
        :param f2: La deuxième formule.
        """
        self.f1 = f1
        self.f2 = f2

    def __repr__(self):
        """
        Fournit une représentation textuelle de la disjonction (ex: (p | q)).
        """
        return f"({self.f1} | {self.f2})" # Utilisation du pipe ASCII pour "Ou"

class Implique: # Représente ⊃
    """
    Représente l'implication logique (>> ou ⊃).
    """
    def __init__(self, f1, f2):
        """
        Initialise une implication avec l'antécédent et le conséquent.
        :param f1: L'antécédent de l'implication.
        :param f2: Le conséquent de l'implication.
        """
        self.f1 = f1
        self.f2 = f2

    def __repr__(self):
        """
        Fournit une représentation textuelle de l'implication (ex: (p >> q)).
        """
        return f"({self.f1} >> {self.f2})" # Utilisation de ">>" ASCII pour "Implique"

class Necessaire: # Carré (Box) - Représente □
    """
    Représente l'opérateur modal de nécessité (Box ou □).
    """
    def __init__(self, formule):
        """
        Initialise l'opérateur de nécessité avec la formule qu'il modifie.
        :param formule: La formule qui est nécessaire.
        """
        self.formule = formule

    def __repr__(self):
        """
        Fournit une représentation textuelle de l'opérateur de nécessité (ex: Box(p)).
        """
        return f"Box({self.formule})" # Utilisation de "Box" ASCII pour "Nécessaire"

class Possible: # Losange (Diamond) - Représente ◇
    """
    Représente l'opérateur modal de possibilité (Diamond ou ◇).
    """
    def __init__(self, formule):
        """
        Initialise l'opérateur de possibilité avec la formule qu'il modifie.
        :param formule: La formule qui est possible.
        """
        self.formule = formule

    def __repr__(self):
        """
        Fournit une représentation textuelle de l'opérateur de possibilité (ex: Dia(p)).
        """
        return f"Dia({self.formule})" # Utilisation de "Dia" ASCII pour "Possible"

# --- Partie 2: Définition du Modèle de Kripke ---
class ModeleKripke:
    """
    Représente un Modèle de Kripke, qui est une structure pour l'interprétation de la logique modale.
    Un modèle de Kripke M est un triplet (W, R, V) où:
    - W est un ensemble de mondes (self.mondes).
    - R est une relation d'accessibilité entre les mondes (self.relation_R).
    - V est une fonction de valuation qui associe à chaque monde l'ensemble des propositions atomiques qui y sont vraies (self.valuation_V).
    """
    def __init__(self, nom_modele="Mon Modèle"):
        """
        Initialise un Modèle de Kripke vide.
        :param nom_modele: Un nom optionnel pour le modèle.
        """
        self.nom = nom_modele
        self.mondes = set()  # Ensemble des mondes W
        self.relation_R = {} # Dictionnaire représentant la relation R (monde -> ensemble de mondes accessibles)
        self.valuation_V = {} # Dictionnaire représentant la valuation V (monde -> ensemble de noms de propositions vraies)

    def ajouter_monde(self, nom_monde):
        """
        Ajoute un monde au modèle de Kripke.
        Initialise également ses entrées dans la relation d'accessibilité et la valuation.
        :param nom_monde: Le nom du monde à ajouter (chaîne de caractères).
        """
        if nom_monde not in self.mondes:
            self.mondes.add(nom_monde)
            self.relation_R[nom_monde] = set()
            self.valuation_V[nom_monde] = set()

    def ajouter_mondes(self, liste_noms_mondes):
        """
        Ajoute plusieurs mondes au modèle à partir d'une liste.
        :param liste_noms_mondes: Une liste de noms de mondes.
        """
        for nom_monde in liste_noms_mondes:
            self.ajouter_monde(nom_monde)

    def ajouter_relation(self, monde_origine, monde_destination):
        """
        Ajoute une relation d'accessibilité (monde_origine R monde_destination) au modèle.
        Crée les mondes si ils n'existent pas déjà.
        :param monde_origine: Le monde de départ de la relation.
        :param monde_destination: Le monde d'arrivée de la relation.
        """
        if monde_origine not in self.mondes: self.ajouter_monde(monde_origine)
        if monde_destination not in self.mondes: self.ajouter_monde(monde_destination)
        self.relation_R[monde_origine].add(monde_destination)

    def ajouter_proposition_vraie(self, monde, nom_proposition_str):
        """
        Associe une proposition atomique à un monde, indiquant qu'elle est vraie dans ce monde.
        Crée le monde si il n'existe pas déjà.
        :param monde: Le monde où la proposition est vraie.
        :param nom_proposition_str: Le nom de la proposition atomique (chaîne de caractères).
        """
        if monde not in self.mondes: self.ajouter_monde(monde)
        self.valuation_V[monde].add(nom_proposition_str)

    def mondes_accessibles(self, monde):
        """
        Renvoie l'ensemble des mondes accessibles depuis un monde donné selon la relation R.
        :param monde: Le monde dont on veut connaître les successeurs.
        :return: Un ensemble de mondes accessibles.
        """
        return self.relation_R.get(monde, set())

    def est_vraie_prop(self, monde, nom_proposition_str):
        """
        Vérifie si une proposition atomique est vraie dans un monde donné.
        :param monde: Le monde à vérifier.
        :param nom_proposition_str: Le nom de la proposition atomique.
        :return: True si la proposition est vraie dans le monde, False sinon.
        """
        return nom_proposition_str in self.valuation_V.get(monde, set())

    def __repr__(self):
        """
        Fournit une représentation textuelle détaillée du modèle de Kripke.
        """
        representation = f"Modèle de Kripke: {self.nom}\n"
        representation += "------------------------------\n"
        representation += f"Mondes (W): {sorted(list(self.mondes))}\n"
        representation += "Relation d'Accessibilité (R):\n"
        # Affichage trié des relations pour une meilleure lisibilité
        for monde_key in sorted(list(self.relation_R.keys())):
            accessibles = self.relation_R[monde_key]
            if accessibles: representation += f"   {monde_key} -> {sorted(list(accessibles))}\n"
        representation += "Valuation (V) - Propositions vraies:\n"
        # Affichage trié des valuations pour une meilleure lisibilité
        for monde_key in sorted(list(self.valuation_V.keys())):
            props_vraies = self.valuation_V[monde_key]
            if props_vraies: representation += f"   Dans {monde_key}: {sorted(list(props_vraies))}\n"
        # Ajoute une note si aucune proposition n'est vraie dans le modèle (totalement vide)
        if not any(self.valuation_V.values()): representation += "   (Aucune proposition n'est vraie)\n"
        representation += "------------------------------"
        return representation

# --- Partie 3: Fonction d'Évaluation des Formules ---
def evaluer(formule, modele: ModeleKripke, monde_actuel: str) -> bool:
    """
    Évalue la vérité d'une formule modale dans un monde spécifique d'un modèle de Kripke.
    Cette fonction est récursive et gère tous les types de formules définis.
    :param formule: La formule modale à évaluer (objet de type Propos, Non, Et, Ou, Implique, Necessaire, Possible).
    :param modele: Le modèle de Kripke dans lequel l'évaluation est effectuée.
    :param monde_actuel: Le nom du monde actuel où l'évaluation est faite.
    :return: True si la formule est vraie dans le monde actuel du modèle, False sinon.
    :raises ValueError: Si le monde actuel n'existe pas dans le modèle.
    :raises TypeError: Si un type de formule non supporté est rencontré.
    """
    if monde_actuel not in modele.mondes:
        raise ValueError(f"Monde '{monde_actuel}' non trouvé dans le modèle pour l'évaluation.")

    if isinstance(formule, Propos):
        # Une proposition atomique est vraie si elle est dans la valuation du monde actuel.
        return modele.est_vraie_prop(monde_actuel, formule.name)
    elif isinstance(formule, Non):
        # La négation d'une formule est vraie si la formule elle-même est fausse.
        return not evaluer(formule.formule, modele, monde_actuel)
    elif isinstance(formule, Et):
        # Une conjonction est vraie si les deux sous-formules sont vraies.
        return evaluer(formule.f1, modele, monde_actuel) and evaluer(formule.f2, modele, monde_actuel)
    elif isinstance(formule, Ou):
        # Une disjonction est vraie si au moins une des sous-formules est vraie.
        return evaluer(formule.f1, modele, monde_actuel) or evaluer(formule.f2, modele, monde_actuel)
    elif isinstance(formule, Implique):
        # Une implication est vraie si l'antécédent est faux ou le conséquent est vrai (¬P ∨ Q).
        return (not evaluer(formule.f1, modele, monde_actuel)) or evaluer(formule.f2, modele, monde_actuel)
    elif isinstance(formule, Necessaire):
        # L'opérateur de nécessité (□φ) est vrai dans un monde w si φ est vraie dans TOUS les mondes accessibles depuis w.
        mondes_a_verifier = modele.mondes_accessibles(monde_actuel)
        if not mondes_a_verifier:
            # Si le monde actuel n'a pas de successeurs, □φ est trivialement vrai (condition vacue).
            return True
        for monde_accessible in mondes_a_verifier:
            if not evaluer(formule.formule, modele, monde_accessible):
                # Si φ est fausse dans un seul monde accessible, □φ est faux.
                return False
        # Si φ est vraie dans tous les mondes accessibles, □φ est vrai.
        return True
    elif isinstance(formule, Possible):
        # L'opérateur de possibilité (◇φ) est vrai dans un monde w si φ est vraie dans AU MOINS UN monde accessible depuis w.
        mondes_a_verifier = modele.mondes_accessibles(monde_actuel)
        if not mondes_a_verifier:
            # Si le monde actuel n'a pas de successeurs, ◇φ est faux (il n'y a nulle part où φ pourrait être vraie).
            return False
        for monde_accessible in mondes_a_verifier:
            if evaluer(formule.formule, modele, monde_accessible):
                # Si φ est vraie dans au moins un monde accessible, ◇φ est vrai.
                return True
        # Si φ est fausse dans tous les mondes accessibles, ◇φ est faux.
        return False
    else:
        # Gère les types de formules non reconnus.
        raise TypeError(f"Type de formule non supporté: {type(formule)}")

# --- Partie 5: Visualisation (Optionnelle) ---
def visualiser_modele_kripke(modele_kripke, titre_suffix=""):
    """
    Visualise un modèle de Kripke sous forme de graphe dirigé à l'aide de NetworkX et Matplotlib.
    Les mondes sont les nœuds, les relations d'accessibilité sont les arêtes.
    Les propositions vraies dans chaque monde sont affichées dans les étiquettes des nœuds.
    :param modele_kripke: Le modèle de Kripke à visualiser.
    :param titre_suffix: Un suffixe optionnel à ajouter au titre du graphique.
    """
    # Vérifie si les modules nécessaires sont importés.
    global nx, plt 
    if 'nx' not in globals() or 'plt' not in globals():
        print("\nLes bibliothèques networkx et matplotlib sont nécessaires pour la visualisation.")
        print("Assurez-vous qu'elles sont importées au début du script.")
        print("Vous pouvez les installer avec : pip install networkx matplotlib")
        return
    
    G = nx.DiGraph() # Crée un graphe dirigé

    # Ajout des nœuds (mondes) au graphe
    for monde_visu in modele_kripke.mondes:
        # Récupère les propositions vraies pour le monde actuel et les formate pour l'étiquette du nœud.
        props_vraies_str = ", ".join(sorted(list(modele_kripke.valuation_V.get(monde_visu, set()))))
        # Crée l'étiquette du nœud: "Nom du monde\n(propositions vraies)" ou juste "Nom du monde" si aucune proposition.
        label = f"{monde_visu}\n({props_vraies_str})" if props_vraies_str else monde_visu
        G.add_node(monde_visu, label=label) # Ajoute le nœud avec son étiquette

    # Ajout des arêtes (relations d'accessibilité) au graphe
    for origine, destinations in modele_kripke.relation_R.items():
        for dest in destinations:
            G.add_edge(origine, dest) # Ajoute une arête dirigée de l'origine vers la destination

    plt.figure(figsize=(12, 8)) # Crée une nouvelle figure Matplotlib pour le graphique
    
    print("\nUtilisation de 'spring_layout' de NetworkX pour la visualisation (pas de dépendance Graphviz).")
    # Choisit une disposition pour les nœuds du graphe.
    # 'spring_layout' est une disposition algorithmique qui essaie de placer les nœuds de manière équilibrée,
    # simulant des forces de ressort entre eux.
    # k: ajustement de la distance optimale entre les nœuds.
    # iterations: nombre d'itérations de l'algorithme.
    # seed: pour une reproductibilité des résultats de la disposition.
    pos = nx.spring_layout(G, k=1.5, iterations=70, seed=42) 
    
    labels_nodes = nx.get_node_attributes(G, 'label') # Récupère les étiquettes personnalisées des nœuds
    
    # Dessine le graphe
    nx.draw(G, pos, with_labels=False, node_size=4000, node_color="skyblue",
            font_size=9, arrows=True, arrowstyle='-|>', arrowsize=20,
            edge_color='gray', width=1.5)
    # Dessine les étiquettes des nœuds séparément pour plus de contrôle
    nx.draw_networkx_labels(G, pos, labels=labels_nodes, font_size=10, font_weight='bold')
    
    plt.title(f"Visualisation du Modèle de Kripke: {modele_kripke.nom}{titre_suffix}", fontsize=16)
    plt.show() # Affiche le graphique

# --- Partie 4: Application à l'Exercice 2 ---
if __name__ == "__main__":
    # Ce bloc de code s'exécute uniquement lorsque le script est exécuté directement.

    # 1. Définir les propositions atomiques utilisées dans l'exercice
    prop_a = Propos("a")
    prop_b = Propos("b")
    prop_c = Propos("c")
    prop_d = Propos("d")

    # 2. Créer le modèle de Kripke M tel que décrit dans l'Exercice 2
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
    # Ajoute chaque relation au modèle
    for orig, dest in relations_R:
        modele_M.ajouter_relation(orig, dest)

    # Définir la valuation V (quelles propositions sont vraies dans quels mondes)
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
    print(modele_M) # Affiche la représentation textuelle du modèle
    print("\n")

    print("Évaluation des Formules de l'Exercice 2:")
    print("---------------------------------------")
    
    # Formules de l'exercice à évaluer
    # a) M, w1 |= □(◇a ∨ ¬b)
    # Traduction: "Il est nécessaire que (il est possible que 'a' OU 'non b')"
    formule_2a = Necessaire(Ou(Possible(prop_a), Non(prop_b)))
    monde_2a = 'w1'
    resultat_2a = evaluer(formule_2a, modele_M, monde_2a)
    print(f"a) M, {monde_2a} |= {formule_2a}   :   {resultat_2a}")

    # b) M, w2 |= ¬(◇((c ⊃ ¬b) ∨ ◇a))
    # Traduction: "Il n'est PAS possible que ((si 'c' alors 'non b') OU (il est possible que 'a'))"
    formule_2b = Non(Possible(Ou(Implique(prop_c, Non(prop_b)), Possible(prop_a))))
    monde_2b = 'w2'
    resultat_2b = evaluer(formule_2b, modele_M, monde_2b)
    print(f"b) M, {monde_2b} |= {formule_2b}   :   {resultat_2b}")

    # c) M, w3 |= ◇(a ∧ ¬c) 
    # Traduction: "Il est possible que ('a' ET 'non c')"
    formule_2c = Possible(Et(prop_a, Non(prop_c))) 
    monde_2c = 'w3'
    resultat_2c = evaluer(formule_2c, modele_M, monde_2c)
    print(f"c) M, {monde_2c} |= {formule_2c}   :   {resultat_2c}")

    # d) M, w4 |= □(c ∨ d)
    # Traduction: "Il est nécessaire que ('c' OU 'd')"
    formule_2d = Necessaire(Ou(prop_c, prop_d))
    monde_2d = 'w4'
    resultat_2d = evaluer(formule_2d, modele_M, monde_2d)
    print(f"d) M, {monde_2d} |= {formule_2d}   :   {resultat_2d}")

    # e) M, w5 |= ◇( (□(a ∧ c)) ∧ d )
    # Traduction: "Il est possible que ((il est nécessaire que ('a' ET 'c')) ET 'd')"
    formule_2e = Possible(Et(Necessaire(Et(prop_a, prop_c)), prop_d))
    monde_2e = 'w5'
    resultat_2e = evaluer(formule_2e, modele_M, monde_2e)
    print(f"e) M, {monde_2e} |= {formule_2e}   :   {resultat_2e}")
    
    # f) M, w6 |= ¬(□(□((¬c) ∨ (¬b))))
    # Traduction: "Il n'est PAS nécessaire que (il est nécessaire que ('non c' OU 'non b'))"
    formule_2f = Non(Necessaire(Necessaire(Ou(Non(prop_c), Non(prop_b)))))
    monde_2f = 'w6'
    resultat_2f = evaluer(formule_2f, modele_M, monde_2f)
    print(f"f) M, {monde_2f} |= {formule_2f}   :   {resultat_2f}")

    print("\nTentative de visualisation du modèle de l'exercice...")
    # Appelle la fonction de visualisation pour afficher le modèle de Kripke créé.
    visualiser_modele_kripke(modele_M)