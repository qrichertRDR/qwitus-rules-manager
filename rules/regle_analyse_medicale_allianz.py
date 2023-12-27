# ---
# Name: Règle analyse médicale Allianz
# Short Name: regle_analyse_medicale_allianz
# Type: underwriting_type
# ---

# date = date_fin_franchise()
# Changement de la date d'application des 45 jours 
date = date_debut_arret_de_travail()
date = ajouter_jours(date, 46)
if code_de_l_evenement_du_prejudice() == 'maternite':
    return None, None
return 'analyse_medicale_allianz', date
