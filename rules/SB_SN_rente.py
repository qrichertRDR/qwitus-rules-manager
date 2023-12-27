# ---
# Name: Salaire brut + passage net et gestion rupture par tranche de salaire et catégories rente
# Short Name: SB_SN_rente
# Type: benefit
# ---

categorie = compl_categorie_de_rente_d_invalidite()
passage_au_net = param_5_passage_au_net()
taux_r1_rupture = param_6_ta_tb_tc_de_r1_rupture()
taux_r2_rupture = param_6_ta_tb_tc_de_r2_rupture()
taux_r3_rupture = param_6_ta_tb_tc_de_r3_rupture()
rupture = element_couvert_est_beneficiaire()
r1_comme_r2 = param_4_pourcentage_r1_defini_comme_pourcentage_de_r2()
rente_SS = compl_rente_securite_sociale_annuelle()

description = ''
if passage_au_net not in ('r2', 'r3'):
    ajouter_erreur('Type de sinistre non géré (passage au net sur: %s)' % passage_au_net)
if categorie == 'r1':
    if not rupture:
        tauxTA = param_1_pourcentage_ta_r1() if not r1_comme_r2 else param_1_pourcentage_ta_r1() * param_2_pourcentage_ta_r2() / 100
        tauxTB = param_1_pourcentage_tb_r1() if not r1_comme_r2 else param_1_pourcentage_tb_r1() * param_2_pourcentage_ta_r2() / 100
        tauxTC = param_1_pourcentage_tc_r1() if not r1_comme_r2 else param_1_pourcentage_tc_r1() * param_2_pourcentage_ta_r2() / 100
    else:
        tauxTA, tauxTB, tauxTC = taux_r1_rupture.split(',')
        tauxTA, tauxTB, tauxTC = (Decimal(tauxTA), Decimal(tauxTB), Decimal(tauxTC))
        if r1_comme_r2:
            TA_R2, TB_R2, TC_R2 = taux_r2_rupture.split(',')
            TA_R2, TB_R2, TC_R2 = (Decimal(TA_R2), Decimal(TB_R2), Decimal(TC_R2))
            tauxTA = tauxTA * TA_R2 / 100
            tauxTB = tauxTB * TB_R2 / 100
            tauxTC = tauxTC * TC_R2 / 100
    description = 'Calcul sur salaire BRUT + primes:\n'
    tranches = tranche_salaire(['gross_salary', 'salary_bonus'])
elif categorie == 'r2':
    if not rupture:
        tauxTA = param_2_pourcentage_ta_r2()
        tauxTB = param_2_pourcentage_tb_r2()
        tauxTC = param_2_pourcentage_tc_r2()
    else:
        tauxTA, tauxTB, tauxTC = taux_r2_rupture.split(',')
        tauxTA, tauxTB, tauxTC = (Decimal(tauxTA), Decimal(tauxTB), Decimal(tauxTC))
    if param_5_passage_au_net() == 'r2':
        description = 'Calcul sur salaire NET:\n'
        tranches = tranche_salaire(['net_salary'])
    else:
        description = 'Calcul sur salaire BRUT + primes:\n'
        tranches = tranche_salaire(['gross_salary', 'salary_bonus'])
elif categorie == 'r3':
    if not rupture:
        tauxTA = param_3_pourcentage_ta_r3()
        tauxTB = param_3_pourcentage_tb_r3()
        tauxTC = param_3_pourcentage_tc_r3()
    else:
        tauxTA, tauxTB, tauxTC = taux_r3_rupture.split(',')
        tauxTA, tauxTB, tauxTC = (Decimal(tauxTA), Decimal(tauxTB), Decimal(tauxTC))
    if param_5_passage_au_net() == 'r3' or param_5_passage_au_net() == 'r2':
        description = 'Calcul sur salaire NET:\n'
        tranches = tranche_salaire(['net_salary'])
    else:
        description = 'Calcul sur salaire BRUT + primes:\n'
        tranches = tranche_salaire(['gross_salary', 'salary_bonus'])
else:
    ajouter_erreur('Type de sinistre non géré')
    
salaire_de_base = 0
trancheTA, trancheTB, trancheTC = 0, 0, 0
if tauxTA:
    trancheTA = arrondir(tauxTA * tranches['TA'] / 100.0, 0.01)
    salaire_de_base += trancheTA
    description += 'Salaire de base (TA): %s€ = %s * %s€ /100\n' % (trancheTA, tauxTA, tranches['TA'])
if tauxTB:
    trancheTB = arrondir(tauxTB * tranches['TB'] / 100.0, 0.01)
    salaire_de_base += trancheTB
    description += 'Salaire de base (TB): %s€ = %s * %s€ /100\n' % (trancheTB, tauxTB, tranches['TB'])
if tauxTC:
    trancheTC = arrondir(tauxTC * tranches['TC'] / 100.0, 0.01)
    salaire_de_base += trancheTC
    description += 'Salaire de base (TC): %s€ = %s * %s€ /100\n' % (trancheTC, tauxTC, tranches['TC'])

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
periodes = periode_de_rente(date_debut_periode, date_fin_periode)
res = []

# Pas d'indémnisation si rente SS nulle
if not rente_SS:
    salaire_de_base = 0
    description = "Aucune prestation à verser car la rente de la securité sociale est nulle\n"  

description += 'Rente Sécurité Sociale: %s€\n' % compl_rente_securite_sociale_annuelle()
description_copy = description
for date_debut, date_fin, periode_entiere, prorata, unit in periodes:
    description = description_copy
    if not periode_entiere:
        montant_proratise = salaire_de_base / 365 * prorata
        montant_par_unite = salaire_de_base / 365
        montant_reference = (tranches['TA'] + tranches['TB'] + tranches['TC']) / 365 * prorata
        rente_SS_reference = rente_SS / 365 * prorata
        rente_SS_unite = rente_SS / 365
        ajouter_info((date_debut, date_fin))
    else:
        montant_proratise = salaire_de_base / 12 * prorata
        montant_par_unite = salaire_de_base / 12
        montant_reference = (tranches['TA'] + tranches['TB'] + tranches['TC']) / 12 * prorata
        rente_SS_reference = rente_SS / 12 * prorata
        rente_SS_unite = rente_SS / 12
    montant_proratise_deduit = montant_proratise
    # mi temps therapeutique
    montant_mi_temps = montant_de_deduction('part_time', date_debut, date_fin)

    montant_mi_temps_total = 0
    if montant_mi_temps:
        montant_mi_temps_total = arrondir(montant_mi_temps * ((date_fin - date_debut).days + 1), 0.01)
        montant_proratise = arrondir(montant_proratise / 2, 0.01)
        montant_par_unite = arrondir(montant_par_unite / 2, 0.01)
        description += 'Versement employeur - Mi temps thérapeutique: %s€ (montant journalier: %s€)\n\n' % (montant_mi_temps_total, montant_mi_temps)   
    # Limiter à 100% du salaire de base
    if montant_reference < arrondir(montant_proratise, 0.01) + arrondir(rente_SS_reference, 0.01) + montant_mi_temps_total:
        montant_proratise_deduit = arrondir(montant_proratise, 0.01) - arrondir(rente_SS_reference, 0.01) - montant_mi_temps_total
        montant_par_unite = arrondir(montant_par_unite, 0.01) - arrondir(rente_SS_unite, 0.01) - montant_mi_temps_total
        description += 'Limitation à 100 pourcent du salaire soit %s€ %s\n' % arrondir((max(montant_proratise_deduit, 0), 0.01), montant_reference)
    else:
        montant_proratise_deduit = montant_proratise - arrondir(rente_SS_reference, 0.01)
        montant_par_unite = montant_par_unite - arrondir(rente_SS_unite, 0.01)
        description += "Montant proratisé déduit de la rente SS: %s€ - %s€ = %s€\n" % (arrondir(montant_proratise, 0.01), arrondir(rente_SS_reference, 0.01),
            montant_proratise_deduit)
    if montant_proratise_deduit < 0:
        montant_proratise_deduit = 0
    if montant_par_unite < 0:
        montant_par_unite = 0

    res.append({
                'start_date': date_debut,
                'end_date': date_fin,
                'nb_of_unit': prorata,
                'unit': unit,
                'amount': montant_proratise_deduit,
                'base_amount': montant_par_unite,
                'amount_per_unit': montant_par_unite,
                'description': description,
                'extra_details': {
                    'tranche_a': str(trancheTA),
                    'tranche_b': str(trancheTB), 
                    'tranche_c': str(trancheTC),
                    }
                })
return res
