# ---
# Name: Franchise fixe en arrêt total (Maladie AT/MP maternité hospi)
# Short Name: coog_franchise_fixe_en_arret_total_maladie_at_mp_maternite_hospi
# Type: benefit_deductible
# ---

evenement = code_de_l_evenement_du_prejudice()
type_franchise = param_1_type_de_franchise()
nb_jour = param_2_franchise()
franchise_hospi = param_6_franchise_en_cas_d_hospitalisation()
franchise_mp = param_3_franchise_en_cas_de_maladie_professionnelle()
franchise_at = param_4_franchise_en_cas_d_accident_du_travail()
franchise_mater = param_5_franchise_en_cas_de_maternite()

if nombre_jours_hospitalisation_prejudice() > 0:
    nb_jour = franchise_hospi if franchise_hospi is not None else nb_jour
elif evenement == 'maladie_professionnelle':
    nb_jour = franchise_mp if franchise_mp is not None else nb_jour
elif evenement == 'accident_du_travail':
    nb_jour = franchise_at if franchise_at is not None else nb_jour
elif evenement == 'maternite':
    nb_jour = franchise_mater if franchise_mater is not None else nb_jour

return rule_coog_franchise_fixe_toute_nature_d_arret_confondue_pour_un_arret_total(
    type_de_franchise=type_franchise, nombre_de_jours_de_franchise=nb_jour)
