from owlready2 import *

# Charger l'ontologie (votre code précédent)
onto = get_ontology("http://example.org/relations_familiales.owl")

with onto:
    
    # TBOX

    # Conceptets atomiques (classes de base)
    class Human(Thing):
        """La classe de base pour tous les humains."""
        pass

    class Person(Human):
        """Une personne est un humain."""
        pass

    class Female(Person):
        """Une femme est une personne de sexe féminin."""
        pass

    class Male(Person):
        """Un homme est une personne de sexe masculin."""
        pass

    class Woman(Female):
        """Une femme adulte."""
        pass

    class Man(Male):
        """Un homme adulte."""
        pass

    class Parent(Person):
        """Un parent est une personne qui a des enfants."""
        pass

    class Mother(Woman, Parent):
        """Une mère est une femme qui est un parent."""
        pass

    class Father(Man, Parent):
        """Un père est un homme qui est un parent."""
        pass

    class Grandmother(Mother):
        """Une grand-mère est une mère d'un parent."""
        pass

    class Aunt(Woman):
        """Une tante est une femme qui est la sœur d'un parent."""
        pass

    class Uncle(Man):
        """Un oncle est un homme qui est le frère d'un parent."""
        pass

    class Sister(Woman):
        """Une sœur est une femme qui a au moins un frère ou une sœur."""
        pass

    class Brother(Man):
        """Un frère est un homme qui a au moins un frère ou une sœur."""
        pass

    # Définition des rôles atomiques (propriétés d'objet)
    # Les propriétés d’objet définissent les relations entre des instances de concepts.
    class has_parent(ObjectProperty):
        """Relie une personne à son parent."""
        domain = [Person]
        range = [Person]

    class has_child(ObjectProperty):
        """Relie un parent à son enfant."""
        domain = [Person]
        range = [Person]
        inverse_property = has_parent

    class has_descendant(ObjectProperty):
        """Relie une personne à ses descendants (enfants, petits-enfants, etc.)."""
        domain = [Person]
        range = [Person]
        transitive = True  # La relation est transitive
        subproperty_of = [has_child]  # has_child est une sous-propriété de has_descendant

    class has_sibling(ObjectProperty):
        """Relie une personne à son frère ou sa sœur."""
        domain = [Person]
        range = [Person]
        symmetric = True  # La relation est symétrique

    class has_sister(has_sibling):
        """Relie une personne à sa sœur."""
        range = [Woman]
        # Le domaine reste Person, car une personne peut avoir une sœur

    class has_brother(has_sibling):
        """Relie une personne à son frère."""
        range = [Man]
        # Le domaine reste Person, car une personne peut avoir un frère

    # Définition des rôles atomiques (propriétés de données)
    # Les propriétés de données définissent des attributs littéraux pour les individus : nom, âge, etc.
    class has_name(DataProperty):
        """Relie une personne à son nom (une chaîne de caractères)."""
        domain = [Person]
        range = [str]
        functional = True  # Declare the property as functional

    class has_age(DataProperty):
        """Relie une personne à son âge (un entier)."""
        domain = [Person]
        range = [int]
        functional = True  # Declare the property as functional

    # Définition des concepts complexes/composés
    class Mother(Woman, Parent):
        """Une mère est une femme ET un parent."""
        pass

    class Father(Man, Parent):
        """Un père est un homme ET un parent."""
        pass

    class Grandmother(Mother):
        equivalent_to = [onto.Mother & onto.has_child.some(onto.Parent)] #somme il existe
        pass

    class Aunt(Woman):
        equivalent_to = [onto.Woman & onto.has_sibling.some(onto.Parent)]
        pass

    class Uncle(Man):
        equivalent_to = [onto.Man & onto.has_sibling.some(onto.Parent)]
        pass

    class Sister(Woman):
        equivalent_to = [onto.Woman & onto.has_sibling.some(onto.Person)]
        pass

    class Brother(Man):
        equivalent_to = [onto.Man & onto.has_sibling.some(onto.Person)]
        pass

    class ChildlessPerson(Person):
        """Une personne sans enfant est une personne ET n'a pas d'enfant."""
        equivalent_to = [onto.Person & Not(onto.has_child.some(onto.Person))]
        pass

    class PersonWithOnlyMaleChildren(Person):
        """Une personne dont tous les enfants sont des hommes."""
        equivalent_to = [onto.Person & onto.has_child.only(onto.Man)]
        pass

    class PersonWithAtLeastTwoChildren(Person):
        """Une personne qui a au moins deux enfants."""
        equivalent_to = [onto.Person & onto.has_child.min(2, onto.Person)]  #en moins 2 enfants
        pass

    class PersonWithExactlyOneDaughter(Person):
        """Une personne qui a exactement une fille."""
        equivalent_to = [onto.Person & onto.has_child.exactly(1, onto.Woman)]  #=1
        pass

    #  Définition de la ABox (Assertional Box)
    # L'ABox contient les instances des concepts et les relations entre elles

    # Création d'individus (instances des classes)
    alice = Mother("Alice")
    betty = Mother("Betty")
    charles = Brother("Charles")
    doris = Sister("Doris")
    eve = Woman("Eve")

    # Définition des relations entre les individus (utilisation des propriétés d'objet)
    alice.has_child.append(betty)
    alice.has_child.append(charles)
    betty.has_child.append(doris)
    betty.has_child.append(eve)
    charles.has_sibling.append(betty)
    doris.has_sibling.append(eve)
    eve.has_sibling.append(doris)

    # Définition des attributs des individus (utilisation des propriétés de données)
    alice.has_name.append("Alice")
    betty.has_name.append("Betty")
    charles.has_name.append("Charles")
    doris.has_name.append("Doris")
    eve.has_name.append("Eve")

    # Assigning data properties to individuals
    alice.has_age.append(45)
    betty.has_age.append(30)
    charles.has_age.append(25)
    doris.has_age.append(20)
    eve.has_age.append(18)

    # Raisonnement
    # Invoquer un raisonneur pour effectuer des inférences
    sync_reasoner(infer_property_values=True)
    
    # Tests et requêtes
    # Vérifier les types inférés
    print("Types inférés pour Eve :", eve.is_a)
    assert any(isinstance(cls, onto.Woman.__class__) for cls in eve.is_a)

    # Vérifier les relations inférées
    print("Enfants d'Alice :", alice.has_child)
    assert betty in alice.has_child

    print("Parents de Betty :", betty.has_parent)
    assert alice in betty.has_parent

    # Vérifier les instances d'un concept
    print("Sœurs :", list(onto.Sister.instances()))
    assert doris in onto.Sister.instances()

    print("Grands-mères :", list(onto.Grandmother.instances()))
    assert alice in onto.Grandmother.instances()

    # Vérifier les propriétés de données
    print("Nom de Charles :", charles.has_name)
    assert "Charles" in charles.has_name
    
    print("Age de Charles :", charles.has_age)
    assert 25 in charles.has_age

    # Exemple de requête plus complexe : trouver les personnes qui ont au moins un enfant
    parents = [person for person in onto.Person.instances() if person.has_child]
    print("Parents :", parents)
    assert alice in parents

    print("Test de l'inférence de PersonWithExactlyOneDaughter")
    person_with_one_daughter = [p for p in onto.Person.instances() if len(p.has_child) == 1 and any(isinstance(child, onto.Woman) for child in p.has_child)]
    print("Personnes avec exactement une fille : ", person_with_one_daughter)

