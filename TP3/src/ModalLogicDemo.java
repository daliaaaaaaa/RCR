import org.tweetyproject.logics.ml.syntax.*;
import org.tweetyproject.logics.ml.semantics.*;
import org.tweetyproject.logics.pl.syntax.Implication;
import org.tweetyproject.logics.pl.syntax.Proposition;

import javax.swing.*;

public class ModalLogicTest {
    public static void main(String[] args) {
        // Définir propositions
        Proposition p = new Proposition("p");
        Proposition q = new Proposition("q");

        // Créer implication (p → q)
        Implication implication = new Implication(p, q);

        // Créer formule modale : [](p → q)
        Box boxFormula = new Box(implication);

        // Créer mondes
        World w1 = new World("w1");
        World w2 = new World("w2");

        // Créer modèle de Kripke
        KripkeModel model = new KripkeModel();
        model.addWorld(w1);
        model.addWorld(w2);
        model.addAccessibility(w1, w2); // w1 peut accéder à w2

        // Ajouter vérité des propositions dans w2
        model.addEvaluation(w2, p, true);
        model.addEvaluation(w2, q, true);

        // Évaluer dans le monde w1
        //boolean result = model.satisfies(boxFormula, w1);
        //System.out.println("w1 satisfait [](p → q) ? " + result);
    }
}
