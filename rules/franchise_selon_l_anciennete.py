# ---
# Name: Franchise selon l'ancienneté
# Short Name: franchise_selon_l_anciennete
# Type: benefit_deductible
# ---

anciennete = annees_entre(compl_date_d_entree_dans_l_entreprise(), date_de_debut_du_prejudice())

if anciennete == 0:
    nb_jour = param_2_franchise_si_l_anciennete_est_inferieure_a_1_an()
elif anciennete < 5:
    nb_jour = param_3_franchise_si_l_anciennete_est_comprise_entre_1_an_et_5_ans()
elif anciennete < 10:
    nb_jour = param_4_franchise_si_l_anciennete_est_comprise_entre_5_ans_et_10_ans()
elif anciennete < 15:
    nb_jour = param_5_franchise_si_l_anciennete_est_comprise_entre_10_ans_et_15_ans()
elif anciennete < 20:
    nb_jour = param_6_franchise_si_l_anciennete_est_comprise_entre_15_ans_et_20_ans()
elif anciennete < 25:
    nb_jour = param_7_franchise_si_l_anciennete_est_comprise_entre_20_ans_et_25_ans() 
elif anciennete < 30:
    nb_jour = param_8_franchise_si_l_anciennete_est_comprise_entre_25_ans_et_30_ans()
else:
    nb_jour = param_9_franchise_si_l_anciennete_est_superieure_ou_egale_a_30_ans()

type_franchise = param_1_type_de_franchise()
return rule_franchise_base_sur_un_nombre_de_jour(nombre_de_jours_de_franchise=nb_jour, type_de_franchise=type_franchise)
