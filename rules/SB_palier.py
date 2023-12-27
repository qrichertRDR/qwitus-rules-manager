# ---
# Name: Salaire brut par tranche de salaire avec palier
# Short Name: SB_palier
# Type: benefit
# ---

# Pas d'indémnisation si IJSS nulle
IJSS = compl_ijss()
description_initial = ''
date_debut_prejudice = date_de_debut_du_prejudice()
date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
palier = param_3_palier_de_reduction_en_jours()
applicable_sur = param_4_palier_applicable_sur()
evenement = code_de_l_evenement_du_prejudice()
prejudice_professionel = evenement == 'accident_du_travail' or evenement == 'maladie_professionnelle'
palier_applicable = not applicable_sur or (prejudice_professionel and (applicable_sur == 'accident_vie_privee_et_travail' or applicable_sur == 'accident_du_travail')
    or not prejudice_professionel and (applicable_sur == 'accident_vie_privee_et_travail' or applicable_sur == 'accident_de_vie_privee'))
palier_applicable = True
if palier:
    date_changement_palier = ajouter_jours(date_debut_prejudice, palier)
res = []

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
            
# Besoin de découper la période si il y a un palier et que le palier traverse cette période.
if palier and palier_applicable and date_changement_palier <= date_fin_periode and date_changement_palier > date_debut_periode:
    sub_periods = [(date_debut_periode, ajouter_jours(date_changement_palier, -1)), (date_changement_palier, date_fin_periode)]
else:
    sub_periods = [(date_debut_periode, date_fin_periode)]

# Calcul pour chaque sous période (potentiellement deux sous périodes si palier défini)
trancheTA, trancheTB, trancheTC = 0, 0, 0

# Si palier dans la période et pas de changement d'ij de base corrigée: levée une alerte
if len(sub_periods) == 2 and compl_ij_de_base_corrige():
    description_initial = 'ATTENTION: IJ DE BASE CORRIGEE N A PAS CHANGE ALORS QU UN PALIER EST DEFINI AU %s\n' % date_changement_palier
    
for sous_date_debut_periode, sous_date_fin_periode in sub_periods:
    # calcul du montant journalier de base
    description = description_initial
    salaire_de_base = 0
    if palier and palier_applicable and sous_date_debut_periode >= date_changement_palier:
        pourcentage_TA = param_2_pourcentage_ij_ta_reduit()
        pourcentage_TB = param_2_pourcentage_ij_tb_reduit()
        pourcentage_TC = param_2_pourcentage_ij_tc_reduit()
        tranches = tranche_salaire(['gross_salary',  'salary_bonus'])
    else:
        pourcentage_TA = param_1_pourcentage_ij_ta()
        pourcentage_TB = param_1_pourcentage_ij_tb()
        pourcentage_TC = param_1_pourcentage_ij_tc()
        tranches = tranche_salaire(['net_salary'])
        
    if pourcentage_TA:
        trancheTA = arrondir(pourcentage_TA * tranches['TA'] / 100.0, 0.01)
        salaire_de_base += trancheTA
        description += 'Salaire de référence (TA): %s%% * %s€ = %s€\n' % (pourcentage_TA, tranches['TA'], trancheTA)
    if pourcentage_TB:
        trancheTB = arrondir(pourcentage_TB * tranches['TB'] / 100.0, 0.01)
        salaire_de_base += trancheTB
        description += 'Salaire de référence (TB): %s%% * %s€ = %s€\n' % (pourcentage_TB, tranches['TB'], trancheTB)
    if pourcentage_TC:
        trancheTC = arrondir(pourcentage_TC * tranches['TC'] / 100.0, 0.01)
        salaire_de_base += trancheTC
        description += 'Salaire de référence (TC): %s%% * %s€ = %s€\n' % (pourcentage_TC, tranches['TC'], trancheTC)
    description += 'Salaire de référence: %s€\n' % salaire_de_base
    salaire_journalier = arrondir(salaire_de_base / 365, 0.01)
    description += 'Salaire de référence journalier: %s€ / 365 = %s€\n\n' % (salaire_de_base, salaire_journalier)

    # mi temps therapeutique
    montant_mi_temps = montant_de_deduction('part_time', sous_date_debut_periode, sous_date_fin_periode)
    salaire_reduit_moitie = False
    if montant_mi_temps:
        montant_mi_temps_total = montant_mi_temps * ((sous_date_fin_periode - sous_date_debut_periode).days + 1)
        salaire_journalier = arrondir(salaire_journalier / 2, 0.01)
        description += 'Versement employeur - Mi temps thérapeutique: %s€ (montant journalier: %s€)\n\n' % (montant_mi_temps_total, montant_mi_temps)
        salaire_reduit_moitie = True

    # IJSS
    IJSS_total = IJSS * ((sous_date_fin_periode - sous_date_debut_periode).days + 1)
    description += 'Versement sécurité sociale: %s€ (IJSS: %s€)\n\n' % (IJSS_total, IJSS)

    # Limiter à 100% du salaire de base
    if salaire_reduit_moitie:
        description += 'Salaire journalier réduit de moitié: %s€\n' % salaire_journalier
    salaire_reference = tranches['TA'] + tranches['TB'] + tranches['TC']
    limite = arrondir(salaire_reference / 365, 0.01)
    if (trancheTA and limite <= salaire_journalier + montant_mi_temps) or (not trancheTA and salaire_journalier + IJSS + montant_mi_temps):
        salaire_journalier_base = arrondir((tranches['TA'] + tranches['TB'] + tranches['TC']) / 365, 0.01) - IJSS - montant_mi_temps
        description += 'Limitation à 100 pourcent du salaire soit %s€\n\n' % max(salaire_journalier_base, 0)
    else:
        salaire_journalier_base = salaire_journalier - IJSS
        description += "Salaire de base journalier deduit de l'IJSS: %s€ - %s€ = %s€\n\n" % (salaire_journalier, IJSS, salaire_journalier_base)
    if salaire_journalier_base < 0:
        salaire_journalier_base = 0

    if compl_ij_de_base_corrige():
        salaire_journalier_base = compl_ij_de_base_corrige() 
        description = description_initial
        description += 'Salaire de base journalier: %s€\n' % salaire_journalier_base

    res.append({
            'start_date': sous_date_debut_periode,
            'end_date': sous_date_fin_periode,
            'nb_of_unit': (sous_date_fin_periode - sous_date_debut_periode).days + 1,
            'unit': 'day',
            'amount': salaire_journalier_base * ((sous_date_fin_periode - sous_date_debut_periode).days + 1),
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
            })
return res
