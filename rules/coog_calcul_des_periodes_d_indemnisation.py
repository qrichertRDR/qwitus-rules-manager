# ---
# Name: Calcul des périodes d'indemnisation
# Short Name: coog_calcul_des_periodes_d_indemnisation
# Type: benefit
# ---

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
traitement_journalier_base = param_traitement_journalier_de_base()
description = param_description()

return ([{
            'start_date': date_debut_periode,
            'end_date': date_fin_periode,
            'nb_of_unit': (date_fin_periode - date_debut_periode).days + 1,
            'unit': 'day',
            'amount': traitement_journalier_base * ((date_fin_periode - date_debut_periode).days + 1),
            'base_amount': traitement_journalier_base,
            'amount_per_unit': traitement_journalier_base,
            'description': description.encode('utf-8'),
            'limit_date': None,
            'extra_details': {
                'tranche_a': param_tranche_ta(),
                'tranche_b': param_tranche_tb(), 
                'tranche_c': param_tranche_tc(),
                'ijss': param_ijss(),
                }
            }])
