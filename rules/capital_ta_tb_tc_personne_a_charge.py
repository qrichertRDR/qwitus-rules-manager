# ---
# Name: Capital TA TB TC personne à charge
# Short Name: capital_ta_tb_tc_personne_a_charge
# Type: benefit
# ---

# calcul du montant journalier de base
description = ''
tranches = tranche_salaire(['gross_salary',  'salary_bonus'])
capital = 0
part = part_beneficiaire()
trancheTA, trancheTB, trancheTC = 0, 0, 0
pourcentage_TA = param_1_pourcentage_ta_assure_seul()  
pourcentage_TB = param_1_pourcentage_tb_assure_seul()
pourcentage_TC = param_1_pourcentage_tc_assure_seul()
pourcentage_TA_a_charge = param_2_pourcentage_de_ta_de_majoration_par_personne_supplementaire()  
pourcentage_TB_a_charge = param_2_pourcentage_de_tb_de_majoration_par_personne_supplementaire()
pourcentage_TC_a_charge = param_2_pourcentage_de_tc_de_majoration_par_personne_supplementaire()

if compl_type_de_beneficiaire() in ('beneficiaire_non_a_charge', 'beneficiaire_a_charge'):
    if pourcentage_TA and tranches['TA']:
        trancheTA = arrondir(pourcentage_TA * tranches['TA'] / 100.0, 0.01)
        capital += trancheTA
        description += 'Capital sur la tranche TA: %s%% * %s€ = %s€\n' % (pourcentage_TA, tranches['TA'], trancheTA)
    if pourcentage_TB and tranches['TB']:
        trancheTB = arrondir(pourcentage_TB * tranches['TB'] / 100.0, 0.01)
        capital += trancheTB
        description += 'Capital sur la tranche TB: %s%% * %s€ = %s€\n' % (pourcentage_TB, tranches['TB'], trancheTB)
    if pourcentage_TC and tranches['TC']:
        trancheTC = arrondir(pourcentage_TC * tranches['TC'] / 100.0, 0.01)
        capital += trancheTC
        description += 'Capital sur la tranche TC: %s%% * %s€ = %s€\n' % (pourcentage_TC, tranches['TC'], trancheTC)
    description += 'Capital de base total: %s€\n\n' % capital

    PASS = table_pmss(date_de_debut_du_prejudice()) * 12
    minimum = PASS * param_capital_minimum_en_pourcentage_du_pass_() / 100
    if capital < minimum:
        capital = minimum
        description += 'Capital minimum appliqué: %s%% * %s€ = %s€\n\n' % (param_capital_minimum_en_pourcentage_du_pass_(), PASS, capital)

    evenement = code_de_l_evenement_du_prejudice()
    if evenement in ['accident', 'accident_du_travail']:
        capital *= 2
        description += 'Doublement du capital en cas d''accident: s€\n' % capital
    
    capital_total = capital
    capital = arrondir(capital * part, 0.01)
    description += 'Capital décès du bénéficiaire (part de %s%%): %s€ * %s%% = %s€\n\n' % (part * 100, capital_total, part * 100, capital)

if compl_type_de_beneficiaire() in ('non_beneficiaire_a_charge', 'beneficiaire_a_charge'):
    capital_majoration = 0
    if pourcentage_TA_a_charge and tranches['TA']:
        trancheTA = arrondir(pourcentage_TA_a_charge * tranches['TA'] / 100.0, 0.01)
        capital_majoration += trancheTA
        description += 'Majoration personne à charge sur la tranche TA: %s%% * %s€ = %s€\n' % (pourcentage_TA_a_charge, tranches['TA'], trancheTA)
    if pourcentage_TB_a_charge and tranches['TB']:
        trancheTB = arrondir(pourcentage_TB_a_charge * tranches['TB'] / 100.0, 0.01)
        capital_majoration += trancheTB
        description += 'Majoration personne à charge sur la tranche TB: %s%% * %s€ = %s€\n' % (pourcentage_TB_a_charge, tranches['TB'], trancheTB)
    if pourcentage_TC_a_charge and tranches['TC']:
        trancheTC = arrondir(pourcentage_TC_a_charge * tranches['TC'] / 100.0, 0.01)
        capital_majoration += trancheTC
        description += 'Majoration personne à charge sur la tranche TC: %s%% * %s€ = %s€\n' % (pourcentage_TC_a_charge, tranches['TC'], trancheTC)
    description += 'Majoration total personne à charge: %s€\n\n' % capital_majoration
    if compl_type_de_beneficiaire() == 'beneficiaire_a_charge':
        description += 'Capital décès total: %s€ + %s€ = %s€\n\n' % (capital, capital_majoration, capital + capital_majoration)
    capital += capital_majoration

debut = date_de_debut_du_prejudice()
fin = date_debut_periode_indemnisation()

return [{
    'start_date': debut,
    'end_date': fin,
    'nb_of_unit': 1,
    'unit': 'day',
    'amount': capital,
    'amount_per_unit': capital,
    'base_amount': capital,
    'description' : description,  
    'extra_details': {
                'montant_capital_base': capital,
                'montant_revalorisation_eckert': 0, 
                'montant_penalite_eckert': 0,
                }
    }]
