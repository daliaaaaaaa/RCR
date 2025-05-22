import sys
from itertools import chain, combinations

sys.stdout.reconfigure(encoding='utf-8')

# ---------- Représentation logique ----------

class Formula:
    def __init__(self, expr):
        self.expr = expr.strip()

    def __repr__(self):
        return self.expr

    def __eq__(self, other):
        return isinstance(other, Formula) and self.expr == other.expr

    def __hash__(self):
        return hash(self.expr)

    def negation(self):
        return Formula(self.expr[1:] if self.expr.startswith("!") else f"!{self.expr}")

# ---------- Règle par défaut ----------

class DefaultRule:
    def __init__(self, prerequisite, justifications, conclusion):
        self.prerequisite = prerequisite
        self.justifications = justifications
        self.conclusion = conclusion

    def __repr__(self):
        preq = str(self.prerequisite) if self.prerequisite else "None"
        justs = ', '.join(map(str, self.justifications))
        return f"{preq} : {justs} / {self.conclusion}"

# ---------- Utilitaires ----------

def powerset(iterable):
    """Génère toutes les sous-ensembles possibles"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def entails(beliefs, formula):
    return formula in beliefs

def consistent(beliefs):
    """Une base est incohérente si elle contient X et !X"""
    formulas = set(beliefs)
    for f in formulas:
        if f.negation() in formulas:
            return False
    return True

# ---------- Théorie par défaut ----------

# Deux bases de faits possibles à cause de la disjonction ¬C et une autre pour  ¬D
facts_list = [
    [Formula("A"), Formula("!C")],
    [Formula("A"), Formula("!D")]
]

defaults = [
    DefaultRule(Formula("A"), [Formula("B")], Formula("C")),    # d1 : A : B / C
    DefaultRule(Formula("A"), [Formula("!C")], Formula("D")),   # d2 : A : ¬C / D
]

# ---------- Raisonneur par défaut ----------

def generate_extensions(facts, defaults):
    extensions = []

    # Génère toutes les combinaisons de règles par défaut
    for candidate_rules in powerset(defaults):
        E = set(facts)
        applied = []

        changed = True
        while changed:
            changed = False
            for d in candidate_rules:
                if d not in applied and \
                   (d.prerequisite is None or d.prerequisite in E) and \
                   all(j not in [f.negation() for f in E] for j in d.justifications):
                    E.add(d.conclusion)
                    applied.append(d)
                    changed = True

        if consistent(E) and E not in extensions:
            extensions.append(E)

    return extensions

# ---------- Affichage des extensions pour la théorie simple ----------

for idx, facts in enumerate(facts_list, 1):
    print(f"\nCas {idx} : Base de faits = {{{', '.join(map(str, facts))}}}")
    extensions = generate_extensions(facts, defaults)
    print("Extensions de Δ = <W, D> :")
    for i, ext in enumerate(extensions, 1):
        print(f"  Extension {i}:")
        for f in sorted(ext, key=lambda x: x.expr):
            print("    ", f)
