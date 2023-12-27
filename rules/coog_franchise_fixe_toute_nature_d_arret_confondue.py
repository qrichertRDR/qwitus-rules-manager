# ---
# Name: Franchise fixe toute nature d'arrêt confondue
# Short Name: coog_franchise_fixe_toute_nature_d_arret_confondue
# Type: benefit_deductible
# ---

nb_jour = param_nombre_de_jours_de_franchise()
type_franchise = param_type_de_franchise()
code_decision = code_decision_eligibilite_prestation()
date_calcul = date_de_debut_du_prejudice()

# Gestion des declarations tardives
if code_decision == 'coog_accepte_pena_franchise_declaration':
    date_calcul = date_declaration_sinistre()
elif code_decision == 'coog_accepte_pena_declaration_date':
    return date_declaration_sinistre()

return rule_coog_franchise_base_sur_un_nombre_de_jour_defaut(type_de_franchise=type_franchise, nombre_de_jours_de_franchise=nb_jour, date_de_prejudice=date_calcul)
