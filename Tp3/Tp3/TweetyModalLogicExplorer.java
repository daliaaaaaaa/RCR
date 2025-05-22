import org.tweetyproject.commons.ParserException;
import org.tweetyproject.logics.ml.parser.MlParser;
import org.tweetyproject.logics.ml.syntax.MlBeliefSet;
import org.tweetyproject.logics.ml.syntax.MlFormula;
import org.tweetyproject.logics.ml.reasoner.SimpleMlReasoner;

public class TweetyModalLogicExplorer {

    public static void main(String[] args) {
        MlParser parser = new MlParser();
        SimpleMlReasoner reasoner = new SimpleMlReasoner();

        System.out.println("=== Début de l'exploration avec Tweety ===");

        // Vous pouvez définir plusieurs scénarios ou bases de connaissances ici.
        // Exemple de scénario 1: Inspiré de votre Figure 3.1
        try {
            System.out.println("\n--- Scénario 1 (Type Figure 3.1) ---");
            MlBeliefSet beliefBase1 = new MlBeliefSet();
            // Rappel de la base de la Figure 3.1 (adaptée pour syntaxe Tweety):
            // <>(A)&&[](B), (<>(A||B)<=>(<>(A)||<>(B))), <>(-)
            // <>(-) peut être interprété comme dia(true)
            beliefBase1.add((MlFormula) parser.parseFormula("(dia(A) && box(B))"));
            beliefBase1.add((MlFormula) parser.parseFormula("((dia(A || B)) <=> (dia(A) || dia(B)))"));
            beliefBase1.add((MlFormula) parser.parseFormula("dia(true)")); // dia(true) pour <>(-)

            System.out.println("Base de connaissances 1: " + beliefBase1);
            System.out.println("Signature de la base 1: " + beliefBase1.getMinimalSignature());

            MlFormula query1 = (MlFormula) parser.parseFormula("dia(A && B)");
            System.out.println("Formule interrogée 1: " + query1);

            boolean result1 = reasoner.query(beliefBase1, query1);
            System.out.println("Réponse à la requête 1: " + result1);

        } catch (ParserException e) {
            System.err.println("Erreur de parsing dans le scénario 1: " + e.getMessage());
        }

        // Exemple de scénario 2: Inspiré de votre Figure 3.2 et 3.3 (Système de sécurité)
        try {
            System.out.println("\n--- Scénario 2 (Système de sécurité - Type Figure 3.2/3.3) ---");
            MlBeliefSet beliefBase2 = new MlBeliefSet();
            // Base de connaissances de la Figure 3.2/3.3:
            // A&&P, (A&&P=><>(A&&P)), (A=><>(P))
            beliefBase2.add((MlFormula) parser.parseFormula("(A && P)"));
            beliefBase2.add((MlFormula) parser.parseFormula("((A && P) => dia(A && P))"));
            beliefBase2.add((MlFormula) parser.parseFormula("(A => dia(P))"));

            System.out.println("Base de connaissances 2: " + beliefBase2);
            System.out.println("Signature de la base 2: " + beliefBase2.getMinimalSignature());

            // Requête 1 pour scénario 2 (Figure 3.2)
            MlFormula query2_1 = (MlFormula) parser.parseFormula("dia(A && P)");
            System.out.println("Formule interrogée 2.1: " + query2_1);
            boolean result2_1 = reasoner.query(beliefBase2, query2_1);
            System.out.println("Réponse à la requête 2.1: " + result2_1);

            // Requête 2 pour scénario 2 (Figure 3.3)
            MlFormula query2_2 = (MlFormula) parser.parseFormula("dia(P)");
            System.out.println("Formule interrogée 2.2: " + query2_2);
            boolean result2_2 = reasoner.query(beliefBase2, query2_2);
            System.out.println("Réponse à la requête 2.2: " + result2_2);

        } catch (ParserException e) {
            System.err.println("Erreur de parsing dans le scénario 2: " + e.getMessage());
        }

        // Comment utiliser ce code pour explorer les concepts du TD N°2 :
        // 1. Exercice 1 & 5 (Axiomes et propriétés de R):
        //    Vous pouvez ajouter des axiomes modaux à une MlBeliefSet.
        //    Par exemple, pour la symétrie (B: p => box(dia(p)) ou T: box(p) => p), etc.
        //    Exemple : beliefBaseAxioms.add((MlFormula) parser.parseFormula("(A => box(dia(A)))"));
        //    Ensuite, interrogez des formules pour voir leurs conséquences sous ces axiomes.
        //    Tweety ne vous *montrera* pas que R est symétrique, mais raisonnera *comme si* elle l'était
        //    si vous incluez l'axiome B.

        // 2. Exercice 2 & 4 (Évaluation de formules dans un modèle):
        //    Tweety ne permet pas de définir explicitement un modèle Kripke (W, R, V) et d'évaluer
        //    directement une formule dans un monde spécifique de CE modèle fixe via SimpleMlReasoner.
        //    SimpleMlReasoner vérifie la conséquence logique à partir d'un ensemble d'axiomes (MlBeliefSet).
        //    Pour simuler, vous pourriez créer une base de connaissances qui essaie de caractériser
        //    les propriétés d'un modèle ou d'un monde, puis interroger.

        // 3. Exercice 3 (Traduction en logique modale):
        //    Une fois les phrases traduites en formules modales, vous pouvez les utiliser
        //    dans des bases de connaissances ou comme requêtes.
        //    Ex: "Les Français savent que..." -> "box_Francais(coronavirus_fleau)"

        // 4. Exercice 6 (Logique S5):
        //    Vous pouvez créer une base de connaissances avec les axiomes de S5 (K, T, B, 4, 5 - ou K, T, 5).
        //    Par exemple, T: box(A) => A;   5: dia(A) => box(dia(A))
        //    Puis vérifier si certaines théorèmes de S5 sont bien dérivables.
        //    Exemple pour S5:
        try {
            System.out.println("\n--- Scénario 3 (Exploration type S5) ---");
            MlBeliefSet s5_axioms = new MlBeliefSet();
            s5_axioms.add((MlFormula) parser.parseFormula("(box(X) => X)")); // Axiome T
            s5_axioms.add((MlFormula) parser.parseFormula("(dia(X) => box(dia(X)))")); // Axiome 5 (ou E)
            // L'axiome K (box(X=>Y)=>(box(X)=>box(Y))) et la règle de nécessitation
            // sont implicitement gérés par le raisonneur pour la logique K de base.

            System.out.println("Axiomes S5 (T et 5 ajoutés): " + s5_axioms);
            // Testons un théorème de S5, par exemple : dia(box(A)) => box(A) (ce n'est pas un théorème standard,
            // mais plutôt box(A) => A ou A => dia(A). Testons box(A) => A, qui est T)
            MlFormula s5_test_theorem = (MlFormula) parser.parseFormula("(box(A) => A)");
            System.out.println("Test d'un axiome comme requête: " + s5_test_theorem);
            // Note: interroger un axiome contre une base le contenant trivialement le prouvera.
            // Il serait plus pertinent d'interroger des formules plus complexes.
            // Par exemple, si S5 valide p => []<>p, vous pourriez essayer de voir si
            // (A => box(dia(A))) est une conséquence des axiomes T et 5 (et K implicite).
            // Souvent, les raisonneurs modaux sont configurés pour une logique spécifique (K, T, S4, S5).
            // SimpleMlReasoner est pour la logique K. Pour des logiques plus fortes comme S5,
            // il faut s'assurer que le raisonneur les supporte ou ajouter les axiomes correspondants
            // à la base de connaissances.

            boolean result_s5 = reasoner.query(s5_axioms, s5_test_theorem);
            System.out.println("Réponse requête S5: " + result_s5);


        } catch (ParserException e) {
            System.err.println("Erreur de parsing dans le scénario S5: " + e.getMessage());
        }


        System.out.println("\n=== Fin de l'exploration ===");
    }
}