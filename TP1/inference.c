#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int run_ubcsat(const char *cnf_file) {
    char command[256];
    snprintf(command, sizeof(command), "ubcsat -alg saps -i %s -solve", cnf_file);

    printf("Exécution de la commande : %s\n", command); // Debug

    FILE *pipe = popen(command, "r");
    if (!pipe) {
        perror("Erreur lors de l'exécution de UBCSAT");
        exit(EXIT_FAILURE);
    }

    char buffer[128];
    int result = -1; // -1 = erreur, 0 = SAT, 1 = UNSAT

    while (fgets(buffer, sizeof(buffer), pipe) != NULL) {
        printf("Sortie de UBCSAT : %s", buffer); // Debug

        // Détecter si une solution a été trouvée (SAT)
        if (strstr(buffer, "Solution found for -target 0")) {
            result = 0; // SAT
            break;
        }

        // Détecter si la formule est UNSAT
        if (strstr(buffer, "UNSATISFIABLE")) {
            result = 1; // UNSAT
            break;
        }
    }

    pclose(pipe);
    return result;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <fichier_CNF> <littéral_phi>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *cnf_file = argv[1]; // Fichier CNF de la base de connaissances
    const char *phi = argv[2];     // Littéral à tester

    // Étape 1: Créer un fichier CNF temporaire avec la négation de phi
    char temp_cnf_file[] = "temp_bc.cnf";
    FILE *original_cnf = fopen(cnf_file, "r");
    FILE *temp_cnf = fopen(temp_cnf_file, "w");

    if (!original_cnf || !temp_cnf) {
        perror("Erreur lors de l'ouverture des fichiers");
        return EXIT_FAILURE;
    }

    // Copier le contenu du fichier CNF original dans le fichier temporaire
    char line[256];
    while (fgets(line, sizeof(line), original_cnf)) {
        fputs(line, temp_cnf);
    }

    // Ajouter la négation de phi à la fin du fichier CNF temporaire
    fprintf(temp_cnf, "%s 0\n", phi); // Ajouter la négation de phi

    // Fermer les fichiers
    fclose(original_cnf);
    fclose(temp_cnf);

    printf("Fichier CNF temporaire créé : %s\n", temp_cnf_file); // Debug

    // Étape 2: Appeler UBCSAT sur le fichier CNF temporaire
    int result = run_ubcsat(temp_cnf_file);

    // Étape 3: Interpréter le résultat
    if (result == 1) {
        printf("BC |= %s\n", phi); // UNSAT : BC infère phi
    } else if (result == 0) {
        printf("BC !|= %s\n", phi); // SAT : BC n'infère pas phi
    } else {
        printf("Erreur lors de l'exécution de UBCSAT.\n");
    }

    // Supprimer le fichier CNF temporaire
    remove(temp_cnf_file);

    return EXIT_SUCCESS;
}