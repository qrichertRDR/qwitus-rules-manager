# ---
# Name: Franchise fonction du nombre de jours d'hospitalisation 
# Short Name: franchise_nb_jour_hospi
# Type: benefit_deductible
# ---

type_franchise = param_1_type_de_franchise()
franchise = param_2_franchise()
franchise_hospitalisation = param_3_franchise_hospistalisation()
periode_hospitalisation = param_4_jours_d_hospitalisation()
prejudice_est_AT = code_du_descriteur_du_prejudice() == 'arret_de_travail'
prejudice_nature_est_accident = code_de_l_evenement_du_prejudice() == 'accident'

AT_consecutif_accident = prejudice_est_AT and prejudice_nature_est_accident

delai_hospitalisation_depasse = nombre_jours_hospitalisation_prejudice() > periode_hospitalisation

if AT_consecutif_accident or delai_hospitalisation_depasse:
    return rule_franchise_base_sur_un_nombre_de_jour(nombre_de_jours_de_franchise=franchise_hospitalisation, type_de_franchise=type_franchise)

return rule_franchise_base_sur_un_nombre_de_jour(nombre_de_jours_de_franchise=franchise, type_de_franchise=type_franchise)
