# ---
# Name: Salaire brut par tranche de salaire sans deduction IJSS
# Short Name: SB_sans_ijss
# Type: 
# ---

# Pas d'indémnisation si IJSS nulle
IJSS = compl_ijss()
date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()

# calcul du montant journalier de base
description = ''
tranches = tranche_salaire(['gross_salary',  'salary_bonus'])
salaire_de_base = 0
trancheTA, trancheTB, trancheTC = 0, 0, 0
pourcentage_TA = param_1_pourcentage_ij_ta()
pourcentage_TB = param_1_pourcentage_ij_tb()
pourcentage_TC = param_1_pourcentage_ij_tc()
if pourcentage_TA:
    trancheTA = arrondir(pourcentage_TA * tranches['TA'] / 100.0, 0.01)
    salaire_de_base += trancheTA
    description += 'Salaire de référence (TA): %s * %s€ /100 = %s€\n' % (pourcentage_TA, tranches['TA'], trancheTA)
if pourcentage_TB:
    trancheTB = arrondir(pourcentage_TB * tranches['TB'] / 100.0, 0.01)
    salaire_de_base += trancheTB
    description += 'Salaire de référence (TB): %s * %s€ /100 = %s€\n' % (pourcentage_TB, tranches['TB'], trancheTB)
if pourcentage_TC:
    trancheTC = arrondir(pourcentage_TC * tranches['TC'] / 100.0, 0.01)
    salaire_de_base += trancheTC
    description += 'Salaire de référence (TC): %s * %s€ /100 = %s€\n' % (pourcentage_TC, tranches['TC'], trancheTC)
description += 'Salaire de référence: %s€\n' % salaire_de_base
salaire_journalier = arrondir(salaire_de_base / 365, 0.01)
description += 'Salaire de référence journalier: %s€ / 365 = %s€\n\n' % (salaire_de_base, salaire_journalier)

# mi temps therapeutique
montant_mi_temps = arrondir(montant_de_deduction('mi-temps_therapeutique', date_debut_periode, date_fin_periode), 0.01)
salaire_reduit_moitie = False
if montant_mi_temps:
    montant_mi_temps_total = arrondir(montant_mi_temps * ((date_fin_periode - date_debut_periode).days + 1), 0.01)
    salaire_journalier = arrondir(salaire_journalier / 2, 0.01)
    description += 'Versement employeur - Mi temps thérapeutique: %s€ (montant journalier: %s€)\n\n' % (montant_mi_temps_total, montant_mi_temps)
    salaire_reduit_moitie = True

# IJSS
IJSS_total = IJSS * ((date_fin_periode - date_debut_periode).days + 1)
description += 'Versement sécurité sociale: %s€ (IJSS: %s€)\n\n' % (IJSS_total, IJSS)

# Limiter à 100% du salaire de base
if salaire_reduit_moitie:
    description += 'Salaire journalier réduit de moitie: %s€\n' % salaire_journalier
salaire_reference = tranches['TA'] + tranches['TB'] + tranches['TC']
limite = arrondir(salaire_reference / 365, 0.01)
if (trancheTA and limite <= salaire_journalier + montant_mi_temps) or (not trancheTA and salaire_journalier + IJSS + montant_mi_temps):
    salaire_journalier_base = arrondir((tranches['TA'] + tranches['TB'] + tranches['TC']) / 365, 0.01) - IJSS - montant_mi_temps
    description += 'Limitation à 100 pourcent du salaire soit %s€\n\n' % max(salaire_journalier_base, 0)
else:
    salaire_journalier_base = salaire_journalier
    description += "Salaire de base journalier non-deduit de l'IJSS: %s€\n\n" % (salaire_journalier_base)
if salaire_journalier_base < 0:
    salaire_journalier_base = 0

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
