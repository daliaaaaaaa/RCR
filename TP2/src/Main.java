import java.util.*;
import org.tweetyproject.logics.fol.parser.FolParser; // d’analyser et de convertir des chaînes de caractères en formules syntaxiques et FOL
import org.tweetyproject.logics.fol.reasoner.FolReasoner; //raisonneurs FOL
import org.tweetyproject.logics.fol.reasoner.SimpleFolReasoner; //implementation basé sur table de vérité
import org.tweetyproject.logics.fol.syntax.*;
import org.tweetyproject.logics.commons.syntax.*;



public class Main {
    public static void main(String[] args) throws Exception {
       //initialisation du raisonneur
        FolReasoner.setDefaultReasoner(new SimpleFolReasoner());
        FolReasoner reasoner = FolReasoner.getDefaultReasoner();

        System.out.println("=== Exemple 1 : Oiseaux ===");
        //création de la signature (pour definir les types d'objets)
        FolSignature sig1 = new FolSignature(true); //contient * elements syntaxique
        Sort sortAnimal1 = new Sort("Animal"); //definir type objet
        sig1.add(sortAnimal1);
        Constant mouette = new Constant("mouette", sortAnimal1);
        Constant autruche = new Constant("autruche", sortAnimal1);
        sig1.add(mouette, autruche);
        Predicate flies = new Predicate("Flies", List.of(sortAnimal1));
        Predicate knows = new Predicate("Knows", List.of(sortAnimal1, sortAnimal1));
        sig1.add(flies, knows);

        //analyseurs syntaxique
        FolParser parser = new FolParser();
        parser.setSignature(sig1); //associé a une signature
        FolBeliefSet bs1 = new FolBeliefSet(); //bs1 ensemble de croyances
        bs1.add((FolFormula) parser.parseFormula("!Flies(autruche)"));
        bs1.add((FolFormula) parser.parseFormula("Flies(mouette)"));
        bs1.add((FolFormula) parser.parseFormula("!Knows(mouette,autruche)")); // la mouette ne connait pas l'autruche
        bs1.add((FolFormula) parser.parseFormula("/==(mouette,autruche)")); // les deux sont distincts
        bs1.add((FolFormula) parser.parseFormula("autruche == autruche"));
        System.out.println(bs1);
        System.out.println("Query: Flies(autruche)? " + reasoner.query(bs1, parser.parseFormula("Flies(autruche)")));
        System.out.println("Query: autruche == autruche? " + reasoner.query(bs1, parser.parseFormula("autruche == autruche")));
        System.out.println("Query: mouette /== autruche? " + reasoner.query(bs1, parser.parseFormula("mouette /== autruche")));

        System.out.println("\n=== Exemple 2 : Coquilles ===");
        FolSignature sig2 = new FolSignature(true);
        Sort sortAnimal2 = new Sort("Animal");
        sig2.add(sortAnimal2);
        Constant a = new Constant("a", sortAnimal2);
        Constant b = new Constant("b", sortAnimal2);
        Constant c = new Constant("c", sortAnimal2);
        sig2.add(a, b, c);
        Predicate ceph = new Predicate("ceph", List.of(sortAnimal2));
        Predicate naut = new Predicate("naut", List.of(sortAnimal2));
        Predicate mol = new Predicate("mol", List.of(sortAnimal2));
        Predicate acoq = new Predicate("acoq", List.of(sortAnimal2));
        sig2.add(ceph, naut, mol, acoq);

        parser.setSignature(sig2);
        FolBeliefSet bs2 = new FolBeliefSet();
        bs2.add((FolFormula) parser.parseFormula("forall X: (naut(X) => ceph(X))"));
        bs2.add((FolFormula) parser.parseFormula("forall X: (ceph(X) => mol(X))"));
        bs2.add((FolFormula) parser.parseFormula("forall X: ((mol(X) && !(ceph(X) && !naut(X))) => acoq(X))"));
        bs2.add((FolFormula) parser.parseFormula("forall X: ((ceph(X) && !naut(X)) => !acoq(X))"));
        bs2.add((FolFormula) parser.parseFormula("forall X: (naut(X) => acoq(X))"));
        bs2.add((FolFormula) parser.parseFormula("naut(a)"));
        bs2.add((FolFormula) parser.parseFormula("ceph(b)"));
        bs2.add((FolFormula) parser.parseFormula("mol(c)"));
        System.out.println(bs2);
        System.out.println("Query: acoq(a)? " + reasoner.query(bs2, parser.parseFormula("acoq(a)")));
        System.out.println("Query: acoq(b)? " + reasoner.query(bs2, parser.parseFormula("acoq(b)")));
        System.out.println("Query: !acoq(c)? " + reasoner.query(bs2, parser.parseFormula("!acoq(c)")));

        System.out.println("\n=== Exemple 3 : Légumes ===");
        FolSignature sig3 = new FolSignature(true);
        Sort veg = new Sort("Vegetable");
        sig3.add(veg);
        Constant tomato = new Constant("tomato", veg);
        Constant carrot = new Constant("carrot", veg);
        Constant broccoli = new Constant("broccoli", veg);
        sig3.add(tomato, carrot, broccoli);
        Predicate edible = new Predicate("edible", List.of(veg));
        Predicate red = new Predicate("red", List.of(veg));
        Predicate green = new Predicate("green", List.of(veg));
        sig3.add(edible, red, green);

        parser.setSignature(sig3);
        FolBeliefSet bs3 = new FolBeliefSet();
        bs3.add((FolFormula) parser.parseFormula("forall X: (red(X) => edible(X))"));
        bs3.add((FolFormula) parser.parseFormula("forall X: (green(X) => edible(X))"));
        bs3.add((FolFormula) parser.parseFormula("forall X: (edible(X) => (red(X) || green(X)))"));
        bs3.add((FolFormula) parser.parseFormula("forall X: (red(X) && green(X))"));
        bs3.add((FolFormula) parser.parseFormula("edible(tomato)"));
        bs3.add((FolFormula) parser.parseFormula("edible(carrot)"));
        bs3.add((FolFormula) parser.parseFormula("!edible(broccoli)"));
        System.out.println(bs3);
        System.out.println("Query: edible(tomato)? " + reasoner.query(bs3, parser.parseFormula("edible(tomato)")));
        System.out.println("Query: edible(carrot)? " + reasoner.query(bs3, parser.parseFormula("edible(carrot)")));
        System.out.println("Query: !edible(broccoli)? " + reasoner.query(bs3, parser.parseFormula("!edible(broccoli)")));
        System.out.println("Query: exists X: (red(X) && green(X))? " + reasoner.query(bs3, parser.parseFormula("exists X: (red(X) && green(X))")));


        System.out.println("\n=== Exemple 4 : Fruits sucrés et juteux ===");

        // Création de la signature
        FolSignature sig4 = new FolSignature(true);
        Sort sortFruit = new Sort("Fruit");
        sig4.add(sortFruit);

        // Constantes : fraise, banane, citron
        Constant fraise = new Constant("fraise", sortFruit);
        Constant banane = new Constant("banane", sortFruit);
        Constant citron = new Constant("citron", sortFruit);
        sig4.add(fraise, banane, citron);

        // Prédicats
        Predicate sucre = new Predicate("sucre", List.of(sortFruit));
        Predicate juteux = new Predicate("juteux", List.of(sortFruit));
        Predicate tropical = new Predicate("tropical", List.of(sortFruit));
        Predicate fruitAime = new Predicate("fruit_aime", List.of(sortFruit));
        sig4.add(sucre, juteux, tropical, fruitAime);

        parser.setSignature(sig4);
        FolBeliefSet bs4 = new FolBeliefSet();

        // Règles
        bs4.add((FolFormula) parser.parseFormula("forall X: ((sucre(X) && juteux(X)) => fruit_aime(X))"));
        bs4.add((FolFormula) parser.parseFormula("forall X: (tropical(X) => juteux(X))"));

        // Faits
        bs4.add((FolFormula) parser.parseFormula("sucre(fraise)"));
        bs4.add((FolFormula) parser.parseFormula("juteux(fraise)"));
        bs4.add((FolFormula) parser.parseFormula("sucre(banane)"));
        bs4.add((FolFormula) parser.parseFormula("tropical(banane)"));
        bs4.add((FolFormula) parser.parseFormula("!sucre(citron)"));

        // Requêtes
        System.out.println(bs4);
        System.out.println("Query: fruit_aime(fraise)? " + reasoner.query(bs4, parser.parseFormula("fruit_aime(fraise)")));
        System.out.println("Query: fruit_aime(banane)? " + reasoner.query(bs4, parser.parseFormula("fruit_aime(banane)")));
        System.out.println("Query: !fruit_aime(citron)? " + reasoner.query(bs4, parser.parseFormula("!fruit_aime(citron)")));
        System.out.println("Query: exists X: (sucre(X) && juteux(X))? " + reasoner.query(bs4, parser.parseFormula("exists X: (sucre(X) && juteux(X))")));

    }
}
