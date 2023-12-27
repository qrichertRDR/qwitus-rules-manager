# ---
# Name: Franchise relais convention
# Short Name: coog_franchise_relais_conventation
# Type: benefit_deductible
# ---

# La donnée complémentaire de date d'effet d'indemnisation doit être définie sur la prestation collective.
franchise_min = param_1_nombre_de_jours_de_franchise()
date_indemnisation = compl_date_d_effet_d_indemnisation()

# Calcul de la date de franchise renseignée et du nombre de jours
date_franchise = ajouter_jours(date_indemnisation or date_de_calcul(), -1)

if franchise_min:
    # Calcul de la franchise minimale
    date_franchise_min = rule_coog_franchise_base_sur_un_nombre_de_jour_defaut(
        nombre_de_jours_de_franchise=franchise_min, type_de_franchise='continue', date_de_prejudice=None)
    # Utilisation de la plus grande franchise
    if date_franchise_min > date_franchise:
        date_franchise = date_franchise_min
return date_franchise
