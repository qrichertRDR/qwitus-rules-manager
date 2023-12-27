# ---
# Name: Franchise basée sur un nombre de jours
# Short Name: coog_franchise_base_sur_un_nombre_de_jour_defaut
# Type: benefit_deductible
# ---

# gestion de la rechute
date_prejudice = param_date_de_prejudice() or date_de_debut_du_prejudice()
if est_une_rechute():
    return ajouter_jours(date_prejudice, -1)

# recherche des jours de franchise déjà utilisés
nb_jour = param_nombre_de_jours_de_franchise()
if param_type_de_franchise() == 'cumulee_sur_365_jours':
    date_fin = date_prejudice
    date_fin = ajouter_jours(date_fin, -1)
    date_debut = ajouter_jours(date_fin, -365)
    nb_franchise_cumulee = nb_jour_franchise(date_debut, date_fin)
    nb_jour -= nb_franchise_cumulee
elif param_type_de_franchise() == '12_mois_glissants':
    date_fin = date_prejudice
    date_fin = ajouter_jours(date_fin, -1)
    date_debut = ajouter_mois(date_fin, -12)
    nb_franchise_cumulee = nb_jour_franchise(date_debut, date_fin)
    nb_jour -= nb_franchise_cumulee
elif param_type_de_franchise() == 'cumulee_sur_annee_civile':
    date_fin = date_prejudice
    date_fin = ajouter_jours(date_fin, -1)
    date_debut = datetime.date(date_prejudice.year, 1, 1)
    nb_franchise_cumulee = nb_jour_franchise(date_debut, date_fin)
    nb_jour -= nb_franchise_cumulee
    
nb_jour = max(nb_jour, 0)
return ajouter_jours(date_prejudice, nb_jour - 1)
