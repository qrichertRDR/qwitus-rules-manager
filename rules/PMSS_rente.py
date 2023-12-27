# ---
# Name: Indémnisation basé sur le PMSS Rente
# Short Name: PMSS_rente
# Type: benefit
# ---

# calcul du montant journalier de base
description = ''
tranches = tranche_salaire(['gross_salary'])
salaire_de_base = 0
trancheTA, trancheTB, trancheTC = 0, 0, 0
pourcentage_PMSS = param_1_pourcentage_du_pmss_pour_r1()
description += 'Salaire de base: %s\n' % salaire_de_base
salaire_journalier = arrondir(salaire_de_base / 365, 0.01)
description += 'Salaire de base journalier: %s€ = %s€ / 365\n' % (salaire_journalier, salaire_de_base)

# mi temps therapeutique
montant_mi_temps = compl_salaire_journalier_mi_temps_therapeutique()
if montant_mi_temps:
    salaire_journalier = arrondir(salaire_journalier / 2, 0.01)
    description += 'Mi temps thérapeutique: %s€\n' % montant_mi_temps
    
# Limiter à 100% du salaire de base
IJSS = compl_ijss()
description += 'IJSS: %s€\n' % IJSS
salaire_reference = tranches['TA'] + tranches['TB'] + tranches['TC']
if montant_mi_temps:
    salaire_reference = arrondir(salaire_reference / 2, 0.01)
limite = arrondir(salaire_reference / 365, 0.01)
if (trancheTA and limite <= salaire_journalier + montant_mi_temps) or (not trancheTA and salaire_journalier + IJSS + montant_mi_temps):
    salaire_journalier_base = arrondir((tranches['TA'] + tranches['TB'] + tranches['TC']) / 365, 0.01) - IJSS - montant_mi_temps
    description += 'Limitation à 100 pourcent du salaire soit %s€\n' % max(salaire_journalier_base, 0)
else:
    salaire_journalier_base = salaire_journalier - IJSS
    description += "Salaire de base journalier déduit de l'IJSS: %s€ = %s€ - %s€\n" % (salaire_journalier_base, salaire_journalier, IJSS)
if salaire_journalier_base < 0:
    salaire_journalier_base = 0


date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
return ([{
            'start_date': date_debut_periode,
            'end_date': date_fin_periode,
            'nb_of_unit': (date_fin_periode - date_debut_periode).days + 1,
            'unit': 'day',
            'amount': salaire_journalier_base * ((date_fin_periode - date_debut_periode).days + 1),
            'base_amount': salaire_journalier_base,
            'amount_per_unit': salaire_journalier_base,
            'description': description,
            'limit_date': None,
            'extra_details': {
                'tranche_a': str(trancheTA),
                'tranche_b': str(trancheTB), 
                'tranche_c': str(trancheTC),
                'ijss': str(IJSS)
                }
            }])
