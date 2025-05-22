import sys
from itertools import chain, combinations

# Assure que les caractères spéciaux (comme les accents) s'affichent correctement
sys.stdout.reconfigure(encoding='utf-8')

# ---------- Représentation logique ----------

class Formula:
    def __init__(self, expr):
        # Stocke l'expression logique (ex: "A", "!C", etc.)
        self.expr = expr.strip()

    def __repr__(self):
        # Affichage lisible de la formule
        return self.expr

    def __eq__(self, other):
        # Deux formules sont égales si leur texte est le même
        return isinstance(other, Formula) and self.expr == other.expr

    def __hash__(self):
        # Permet d'utiliser des formules dans des ensembles ou dictionnaires
        return hash(self.expr)

    def negation(self):
        # Retourne la négation de la formule
        # Si déjà négée (!X), enlève le "!", sinon ajoute "!"
        return Formula(self.expr[1:] if self.expr.startswith("!") else f"!{self.expr}")

# ---------- Règle par défaut ----------

class DefaultRule:
    def __init__(self, prerequisite, justifications, conclusion):
        # Initialise une règle par défaut avec :
        # - un prérequis (Formula)
        # - des justifications (liste de Formulas)
        # - une conclusion (Formula)
        self.prerequisite = prerequisite
        self.justifications = justifications
        self.conclusion = conclusion

    def __repr__(self):
        # Affichage lisible de la règle
        preq = str(self.prerequisite) if self.prerequisite else "None"
        justs = ', '.join(map(str, self.justifications))
        return f"{preq} : {justs} / {self.conclusion}"

# ---------- Utilitaires ----------

def powerset(iterable):
    """Génère toutes les sous-ensembles possibles d'un ensemble."""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def entails(beliefs, formula):
    """Vérifie si la formule est dans les croyances."""
    return formula in beliefs

def consistent(beliefs):
    """
    Vérifie la cohérence d’un ensemble de croyances.
    Il est incohérent si une formule et sa négation y sont présentes.
    """
    formulas = set(beliefs)
    for f in formulas:
        if f.negation() in formulas:
            return False
    return True

# ---------- Théorie par défaut ----------

# Deux bases de faits différentes à cause de la disjonction (!C ou !D)
facts_list = [
    [Formula("A"), Formula("!C")],  # Cas 1
    [Formula("A"), Formula("!D")]   # Cas 2
]

# Deux règles par défaut
defaults = [
    DefaultRule(Formula("A"), [Formula("B")], Formula("C")),    # d1 : A : B / C
    DefaultRule(Formula("A"), [Formula("!C")], Formula("D")),   # d2 : A : ¬C / D
]

# ---------- Raisonneur par défaut ----------

def generate_extensions(facts, defaults):
    """
    Génère toutes les extensions possibles pour une base de faits et un ensemble de règles par défaut.
    Une extension est un ensemble de croyances cohérent et maximal.
    """
    extensions = []

    # Génère toutes les combinaisons possibles de règles par défaut
    for candidate_rules in powerset(defaults):
        E = set(facts)  # Copie des faits de départ
        applied = []    # Liste des règles déjà appliquées

        changed = True
        while changed:
            changed = False
            for d in candidate_rules:
                # Si la règle n’a pas été appliquée et que :
                # - le prérequis est présent (ou None)
                # - toutes les justifications ne sont pas contredites
                if d not in applied and \
                   (d.prerequisite is None or d.prerequisite in E) and \
                   all(j not in [f.negation() for f in E] for j in d.justifications):
                    # Appliquer la règle
                    E.add(d.conclusion)
                    applied.append(d)
                    changed = True

        # Vérifie la cohérence et évite les doublons
        if consistent(E) and E not in extensions:
            extensions.append(E)

    return extensions

# ---------- Affichage des extensions pour la théorie simple ----------

# Parcours de chaque base de faits
for idx, facts in enumerate(facts_list, 1):
    print(f"\nCas {idx} : Base de faits = {{{', '.join(map(str, facts))}}}")
    extensions = generate_extensions(facts, defaults)
    print("Extensions de Δ = <W, D> :")
    for i, ext in enumerate(extensions, 1):
        print(f"  Extension {i}:")
        for f in sorted(ext, key=lambda x: x.expr):
            print("    ", f)
