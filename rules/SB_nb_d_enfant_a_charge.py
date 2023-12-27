# ---
# Name: Salaire brut par tranche de salaire selon nb d 'enfant à charge
# Short Name: SB_nb_d_enfant_a_charge
# Type: benefit
# ---

# Pas d'indémnisation si IJSS nulle
IJSS = compl_ijss()
date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
if not IJSS:
    description = "Aucune prestation à verser car l'IJSS est nulle\n"
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

# calcul du montant journalier de base
description = ''
tranches = tranche_salaire(['gross_salary', 'salary_bonus'])
salaire_de_base = 0
trancheTA, trancheTB, trancheTC = 0, 0, 0

nb_enfant_a_charge = compl_nombre_d_enfants_a_charge()
pourcentages = ''
if nb_enfant_a_charge == 0:
    pourcentages = param_1_pourcentage_ta_tb_tc_0_enfant()
elif nb_enfant_a_charge == 1:
    pourcentages = param_2_pourcentage_ta_tb_tc_1_enfant()
elif nb_enfant_a_charge == 2:
    pourcentages = param_3_pourcentage_ta_tb_tc_2_enfant()
elif nb_enfant_a_charge == 3:
    pourcentages = param_4_pourcentage_ta_tb_tc_3_enfant()
elif nb_enfant_a_charge == 3:
    pourcentages = param_5_pourcentage_ta_tb_tc_4_enfant_et_plus()
pourcentage_TA, pourcentage_TB, pourcentage_TC = pourcentages.split(';')
pourcentage_TA = Decimal(pourcentage_TA)
pourcentage_TB = Decimal(pourcentage_TB)
pourcentage_TC = Decimal(pourcentage_TC)

if pourcentage_TA:
    trancheTA = arrondir(pourcentage_TA * tranches['TA'] / 100.0, 0.01)
    salaire_de_base += trancheTA
    description += 'Salaire de base (TA): %s€ = %s * %s€ /100\n' % (trancheTA, pourcentage_TA, tranches['TA'])
if pourcentage_TB:
    trancheTB = arrondir(pourcentage_TB * tranches['TB'] / 100.0, 0.01)
    salaire_de_base += trancheTB
    description += 'Salaire de base (TB): %s€ = %s * %s€ /100\n' % (trancheTB, pourcentage_TB, tranches['TB'])
if pourcentage_TC:
    trancheTC = arrondir(pourcentage_TC * tranches['TC'] / 100.0, 0.01)
    salaire_de_base += trancheTC
    description += 'Salaire de base (TC): %s€ = %s * %s€ /100\n' % (trancheTC, pourcentage_TC, tranches['TC'])
description += 'Salaire de base: %s\n' % salaire_de_base
salaire_journalier = arrondir(salaire_de_base / 365, 0.01)
description += 'Salaire de base journalier: %s€ = %s€ / 365\n' % (salaire_journalier, salaire_de_base)

# mi temps therapeutique
montant_mi_temps = arrondir(montant_de_deduction('part_time', date_debut_periode_indemnisation(), date_fin_periode_indemnisation()), 0.01)
if montant_mi_temps:
    salaire_journalier = arrondir(salaire_journalier / 2, 0.01)
    description += 'Mi temps thérapeutique: %s€\n' % montant_mi_temps
    description += 'Salaire journalier réduit de moitié: %s€\n' % salaire_journalier

# Limiter à 100% du salaire de base
description += 'IJSS: %s€\n' % IJSS
salaire_reference = tranches['TA'] + tranches['TB'] + tranches['TC']
limite = arrondir(salaire_reference / 365, 0.01)

if (trancheTA and limite <= salaire_journalier + montant_mi_temps + IJSS) or (not trancheTA and salaire_journalier + IJSS + montant_mi_temps):
    salaire_journalier_base = arrondir((tranches['TA'] + tranches['TB'] + tranches['TC']) / 365, 0.01) - IJSS - montant_mi_temps
    description += 'Limitation à 100 pourcent du salaire soit %s€\n' % max(salaire_journalier_base, 0)
else:
    salaire_journalier_base = salaire_journalier - IJSS
    description += "Salaire de base journalier déduit de l'IJSS: %s€ = %s€ - %s€\n" % (salaire_journalier_base, salaire_journalier, IJSS)
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
                }
            }])
