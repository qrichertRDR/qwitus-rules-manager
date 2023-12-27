# ---
# Name: Vérification de la déclaration d'arrêt de travail
# Short Name: verification_de_la_declaration_d_arret_de_travail
# Type: process_check
# ---

if not date_de_debut_du_prejudice():
    ajouter_erreur("La date de debut d'arret n'est pas definie")
