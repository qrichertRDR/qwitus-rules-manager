# ---
# Name: Franchise fixe en arrêt total
# Short Name: coog_franchise_fixe_toute_nature_d_arret_confondue_pour_un_arret_total
# Type: benefit_deductible
# ---

nb_jour = param_nombre_de_jours_de_franchise()
type_franchise = param_type_de_franchise()
date_prejudice = date_de_debut_du_prejudice()
code_decision = code_decision_eligibilite_prestation()
date_calcul = date_prejudice

# Gestion des declarations tardives
if code_decision == 'coog_accepte_pena_franchise_declaration':
    date_calcul = date_declaration_sinistre()
elif code_decision == 'coog_accepte_pena_declaration_date':
    return date_declaration_sinistre()

periodes_mtt = periodes_de_deduction('part_time', date_calcul, date_fin_periode_indemnisation())
fin_franchise = rule_coog_franchise_base_sur_un_nombre_de_jour_defaut(type_de_franchise=type_franchise, nombre_de_jours_de_franchise=nb_jour, date_de_prejudice=date_calcul)
for debut_mtt, fin_mtt in periodes_mtt:
    if debut_mtt <= fin_franchise:
        date_calcul = ajouter_jours(fin_mtt, 1)
    else:
       break
    fin_franchise = rule_coog_franchise_base_sur_un_nombre_de_jour_defaut(
        type_de_franchise=type_franchise, nombre_de_jours_de_franchise=nb_jour, date_de_prejudice=date_calcul)
return fin_franchise
