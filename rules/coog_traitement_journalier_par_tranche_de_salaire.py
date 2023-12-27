# ---
# Name: Traitement journalier par tranche de salaire
# Short Name: coog_traitement_journalier_par_tranche_de_salaire
# Type: benefit
# ---

# Pas d'indemnisation si IJSS nulle ou si + de 1095 jours
IJSS = compl_ijss() or Decimal('0.00')
date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
limite = ajouter_jours(date_de_debut_du_prejudice(), 1095)
traitement_de_reference = param_4_traitement_de_reference()
ijss_non_deduite = param_6_sans_deduction_de_l_ijss()
inclusion_mi_temps = param_5_inclusion_du_mi_temps_therapeutique()
limiter_au_net = param_7_limiter_au_net()
description = ''
TA, TB, TC = param_1_pourcentage_ij_ta(), param_2_pourcentage_ij_tb(), param_3_pourcentage_ij_tc()

if (not IJSS and not ijss_non_deduite) or date_fin_periode > limite:
    if not IJSS:
        description += "Aucune prestation à verser car l'IJSS est nulle\n"
    else:
        description += "La période à calculer est au dessus de la limite des 1095 jours, soit le %s" % formater_date(limite)
    return ([{
            'start_date': date_debut_periode,
            'end_date': date_fin_periode,
            'nb_of_unit': (date_fin_periode - date_debut_periode).days + 1,
            'unit': 'day',
            'amount': Decimal(0),
            'base_amount': Decimal(0),
            'amount_per_unit': Decimal(0),
            'description': description,
            }])

# Calcul du traitement de base journalier en fonction des tranches
traitement_journalier_base, traitement_de_reference, trancheTA, trancheTB, trancheTC, description_compl = rule_coog_calcul_du_traitement_de_base_journalier_en_fonction_des_tranches(
    pourcentage_ij_ta=TA, pourcentage_ij_tb=TB, pourcentage_ij_tc=TC, methode_de_traitement_de_reference=traitement_de_reference)
description += description_compl

# Calcul du mi-temps
traitement_journalier_base, montant_mi_temps, description_compl = rule_coog_regle_de_calcul_des_deductions_des_montants_percus(
    traitement_de_base_journalier=traitement_journalier_base, ijss=IJSS, inclusion_du_mi_temps_therapeutique=inclusion_mi_temps, sans_deduction_de_l_ijss=ijss_non_deduite, traitement_de_reference=traitement_de_reference)
description += description_compl

# Calcul des limitations
traitement_journalier_de_base, description_compl = rule_coog_calcul_des_limitations_du_traitement_journalier(
    ijss=IJSS, traitement_de_reference=traitement_de_reference, inclusion_du_mi_temps_therapeutique=inclusion_mi_temps, 
    sans_deduction_de_l_ijss=ijss_non_deduite, montant_du_mi_temps_therapeutique=montant_mi_temps, 
    limiter_au_net=limiter_au_net, traitement_journalier_de_base=traitement_journalier_base)
description += description_compl

# Calcul des périodes d'indemnisation
return rule_coog_calcul_des_periodes_d_indemnisation(
    traitement_journalier_de_base=traitement_journalier_de_base, description=description, tranche_ta=trancheTA, tranche_tb=trancheTB, tranche_tc=trancheTC, ijss=IJSS)
