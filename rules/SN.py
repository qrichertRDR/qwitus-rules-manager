# ---
# Name: Salaire net par tranche de salaire
# Short Name: SN
# Type: benefit
# ---

# Pas d'indémnisation si IJSS nulle ou si + de 1095 jours
IJSS = compl_ijss()
date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
limite = ajouter_jours(date_de_debut_du_prejudice(), 1095)
if not IJSS or date_fin_periode > limite:
    if not IJSS:
        description = "Aucune prestation à verser car l'IJSS est nulle\n"
    else:
        description = "La période à calculer est au dessus de la limite des 1095 jours, soit le %s" % formater_date(limite)
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

# Calcul du montant journalier de base
description = ''

tranches = tranche_salaire(['gross_salary', 'salary_bonus'])
salaire_reference_brut = arrondir(tranches['TA'], 0.01) + arrondir(tranches['TB'], 0.01) + arrondir(tranches['TC'], 0.01)

tranches = tranche_salaire(['net_salary'])
tranches['TA'] = arrondir(tranches['TA'], 0.01)
tranches['TB'] = arrondir(tranches['TB'], 0.01)
tranches['TC'] = arrondir(tranches['TC'], 0.01)
salaire_reference = tranches['TA'] + tranches['TB'] + tranches['TC']
salaire_reference_journalier = arrondir(salaire_reference / 365, 0.01)

salaire_de_base = 0
trancheTA, trancheTB, trancheTC = 0, 0, 0
pourcentage_TA = param_1_pourcentage_ij_ta_SN()
pourcentage_TB = param_1_pourcentage_ij_tb_SN()
pourcentage_TC = param_1_pourcentage_ij_tc_SN()
if pourcentage_TA:
    trancheTA = arrondir(pourcentage_TA * tranches['TA'] / 100.0, 0.01)
    salaire_de_base += trancheTA
    description += 'Salaire de base (TA): %s * %s€ /100 = %s€\n' % (pourcentage_TA, tranches['TA'], trancheTA)
if pourcentage_TB:
    trancheTB = arrondir(pourcentage_TB * tranches['TB'] / 100.0, 0.01)
    salaire_de_base += trancheTB
    description += 'Salaire de base (TB): %s * %s€ /100 = %s€\n' % (pourcentage_TB, tranches['TB'], trancheTB)
if pourcentage_TC:
    trancheTC = arrondir(pourcentage_TC * tranches['TC'] / 100.0, 0.01)
    salaire_de_base += trancheTC
    description += 'Salaire de base (TC): %s * %s€ /100 = %s€\n' % (pourcentage_TC, tranches['TC'], trancheTC)
description += 'Salaire de base: %s€\n' % salaire_de_base
salaire_journalier = arrondir(salaire_de_base / 365, 0.01)
description += 'Salaire de base journalier: %s€ / 365 = %s€\n\n' % (salaire_de_base, salaire_journalier)

# IJSS
IJSS_total = IJSS * ((date_fin_periode - date_debut_periode).days + 1)
description += 'Versement sécurité sociale: %s€ (IJSS: %s€)\n\n' % (IJSS_total, IJSS)

# mi temps therapeutique
montant_mi_temps = montant_de_deduction('part_time', date_debut_periode, date_fin_periode, daily=True, round=False)
if montant_mi_temps:
    montant_mi_temps_total = montant_mi_temps * ((date_fin_periode - date_debut_periode).days + 1)
    montant_mi_temps_total = arrondir(montant_mi_temps_total, 0.01)
    montant_mi_temps = arrondir(montant_mi_temps, 0.01)
    description += 'Versement employeur - Mi temps thérapeutique: %s€ (montant journalier: %s€)\n\n' % (montant_mi_temps_total, montant_mi_temps)
#   ss_avant_mitemps=ijss_avant_mi_temps()
#   description += 'SS avant mi temps: %s€\n' % ss_avant_mitemps
    salaire_journalier = arrondir((salaire_journalier - ijss_avant_mi_temps())/ 2, 0.01)
    limite_mi_temps = salaire_reference_journalier - IJSS - montant_mi_temps
    description += 'Salaire journalier réduit de moitié : %s€\n' % salaire_journalier
    if salaire_journalier > limite_mi_temps:
        salaire_journalier_base = limite_mi_temps
        description += 'Limitation du mi temps thérapeuthique (salaire de reference - IJSS - montant percu en mi-temps: %s€ - %s€ - %s€ = %s€\n' % (
            salaire_reference_journalier, IJSS, montant_mi_temps, salaire_journalier_base)
    else:
        salaire_journalier_base = salaire_journalier
else:
    # Limiter à 100% du salaire de base
    if salaire_reference_journalier < salaire_journalier + IJSS:
        salaire_journalier_base = salaire_reference_journalier - IJSS
        description += 'Limitation à 100 pourcent du salaire soit %s€\n' % max(salaire_journalier_base, 0)
    else:
        salaire_journalier_base = salaire_journalier - IJSS
        description += "Salaire de base journalier deduit de l'IJSS: %s€ - %s€ = %s€\n" % (salaire_journalier, IJSS, salaire_journalier_base)

if salaire_journalier_base < 0:
    salaire_journalier_base = 0

if compl_ij_de_base_corrige():
    salaire_journalier_base = compl_ij_de_base_corrige() 
    description = 'Salaire de base journalier: %s€\n' % salaire_journalier_base

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
                'ijss': str(IJSS),
                'sanction_ijss': str(compl_sanction_ijss()),
                'taux_ta': str(pourcentage_TA),
                'taux_tb': str(pourcentage_TB),
                'taux_tc': str(pourcentage_TC),
                'traitement_base_brut': str(salaire_reference_brut),
                'traitement_base_net': str(salaire_reference),
                }
            }])
