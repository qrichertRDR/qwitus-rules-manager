# ---
# Name: Franchise basé sur un nombre de jour
# Short Name: franchise_base_sur_un_nombre_de_jour
# Type: benefit_deductible
# ---

# gestion de la rechute
date_prejudice = date_de_debut_du_prejudice()
if est_une_rechute():
    return ajouter_jours(date_prejudice,  -1)

# gestion de la declaration tardive
if code_decision_eligibilite_prestation() == 'declaration_tardive_avec_penalite':
    regle_decla_tardive = compl_declaration_tardive()
    if regle_decla_tardive == 'date_decla_plus_franchise':
        date_prejudice = date_declaration_sinistre()
    elif regle_decla_tardive == 'date_decla':
        return ajouter_jours(date_declaration_sinistre(),  -1)

# recherche des jours de franchise déjà utilisés
nb_jour = param_nombre_de_jours_de_franchise()
if param_type_de_franchise() == 'cumulee_sur_365_jours':
    date_fin = date_prejudice
    date_fin = ajouter_jours(date_fin, -1)
    date_debut = ajouter_jours(date_fin, -365)
    nb_franchise_cumulee = nb_jour_franchise(date_debut, date_fin)
    nb_jour -= nb_franchise_cumulee
elif param_type_de_franchise() == 'cumulee_sur_annee_civile':
    date_fin = date_prejudice
    date_fin = ajouter_jours(date_fin, -1)
    date_debut = datetime.date(date_prejudice.year, 1, 1)
    nb_franchise_cumulee = nb_jour_franchise(date_debut, date_fin)
    nb_jour -= nb_franchise_cumulee
    
if nb_jour > 0:
    return ajouter_jours(date_prejudice, nb_jour - 1)
elif nb_jour == 0:
    return ajouter_jours(date_prejudice, nb_jour - 1)
