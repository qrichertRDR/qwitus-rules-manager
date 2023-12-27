# ---
# Name: Franchise toute nature d'arrêt confondue Rente
# Short Name: franchise_globale_rente
# Type: benefit_deductible
# ---

nb_jour = param_2_nombre_de_jours_de_franchise_rente()
nb_jour = 0
type_franchise = param_1_type_de_franchise_rente()
return rule_franchise_base_sur_un_nombre_de_jour(nombre_de_jours_de_franchise=nb_jour, type_de_franchise=type_franchise)
