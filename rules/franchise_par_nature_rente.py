# ---
# Name: Franchise selon la nature de l'arrêt (rente)
# Short Name: franchise_par_nature_rente
# Type: benefit_deductible
# ---

evenement = code_de_l_evenement_du_prejudice()
if nombre_jours_hospitalisation_prejudice() > 0:
     nb_jour = param_6_franchise_en_cas_d_hospitalisation_rente()
elif evenement == 'accident':
    nb_jour = param_4_franchise_en_cas_d_accident_rente()
elif evenement == 'accident_du_travail':
    nb_jour = param_5_franchise_en_cas_d_accident_du_travail_rente()
elif evenement == 'maladie':
    nb_jour = param_2_franchise_en_cas_de_maladie_rente()
elif evenement == 'maladie_professionnelle':
    nb_jour = param_3_franchise_en_cas_de_maladie_professionnelle_rente()
type_franchise = param_1_type_de_franchise_rente()
nb_jour = 0
return rule_franchise_base_sur_un_nombre_de_jour(nombre_de_jours_de_franchise=nb_jour, type_de_franchise=type_franchise)
