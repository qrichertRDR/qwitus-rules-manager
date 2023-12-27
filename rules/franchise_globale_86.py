# ---
# Name: Franchise avec palier de réduction
# Short Name: franchise_globale_86
# Type: benefit_deductible
# ---

type_franchise = param_1_type_de_franchise()
franchise = param_2_franchise()
palier = param_3_palier_en_jours()
franchise_reduite = param_4_franchise_reduite()
periode_en_jours = jours_entre(date_de_debut_du_prejudice(), date_fin_periode_indemnisation())

if periode_en_jours >= palier:
    return rule_franchise_base_sur_un_nombre_de_jour(nombre_de_jours_de_franchise=franchise_reduite, type_de_franchise=type_franchise)
return rule_franchise_base_sur_un_nombre_de_jour(nombre_de_jours_de_franchise=franchise, type_de_franchise=type_franchise)
