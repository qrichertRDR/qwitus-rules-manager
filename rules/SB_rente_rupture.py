# ---
# Name: Salaire brut par tranche de salaire avec rupture rente
# Short Name: SB_rente_rupture
# Type: benefit
# ---

categorie = compl_categorie_de_rente_d_invalidite().lower()
rupture = element_couvert_est_beneficiaire()
rente_SS = compl_rente_securite_sociale_annuelle()

if categorie == 'r1':
    tauxTA = param_1_pourcentage_ta_r1()
    tauxTB = param_1_pourcentage_tb_r1()
    tauxTC = param_1_pourcentage_tc_r1()
    TA_rupture, TB_rupture, TC_rupture = param_5_ta_tb_tc_de_r1_rupture().split(',')
    TA_rupture, TB_rupture, TC_rupture = (Decimal(TA_rupture), Decimal(TB_rupture), Decimal(TC_rupture))
elif categorie == 'r2':
    tauxTA = param_2_pourcentage_ta_r2()
    tauxTB = param_2_pourcentage_tb_r2()
    tauxTC = param_2_pourcentage_tc_r2()
    TA_rupture, TB_rupture, TC_rupture = param_5_ta_tb_tc_de_r2_rupture().split(',')
    TA_rupture, TB_rupture, TC_rupture = (Decimal(TA_rupture), Decimal(TB_rupture), Decimal(TC_rupture))
elif categorie == 'r3':
    tauxTA = param_3_pourcentage_ta_r3()
    tauxTB = param_3_pourcentage_tb_r3()
    tauxTC = param_3_pourcentage_tc_r3()
    TA_rupture, TB_rupture, TC_rupture = param_5_ta_tb_tc_de_r3_rupture().split(',')
    TA_rupture, TB_rupture, TC_rupture = (Decimal(TA_rupture), Decimal(TB_rupture), Decimal(TC_rupture))
else:
    ajouter_erreur('Catégorie du sinistre "%s" non géré' % categorie)
 
if param_4_pourcentage_r1_defini_comme_pourcentage_de_r2() and categorie == 'r1' and not rupture:
    tauxTA = (tauxTA * param_2_pourcentage_ta_r2()) / 100
    tauxTB = (tauxTB * param_2_pourcentage_tb_r2()) / 100
    tauxTC = (tauxTC * param_2_pourcentage_tc_r2()) / 100

if rupture:
    tauxTA, tauxTB, tauxTC = (TA_rupture, TB_rupture, TC_rupture)
    if param_4_pourcentage_r1_defini_comme_pourcentage_de_r2() and categorie == 'r1':
        TA_rupture_r2, TB_rupture_r2, TC_rupture_r2 = param_5_ta_tb_tc_de_r2_rupture().split(',')
        TA_rupture_r2, TB_rupture_r2, TC_rupture_r2  = (Decimal(TA_rupture_r2), Decimal(TB_rupture_r2), Decimal(TC_rupture_r2))       
        tauxTA = (tauxTA * TA_rupture_r2) / 100
        tauxTB = (tauxTB * TB_rupture_r2) / 100
        tauxTC = (tauxTC * TC_rupture_r2) / 100 
    
tranches = tranche_salaire(['gross_salary', 'salary_bonus'])
salaire_de_base = 0
description = ''
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

if compl_rente_annuelle_corrigee():
    salaire_de_base = compl_rente_annuelle_corrigee()

# mi temps therapeutique
date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
montant_mi_temps = arrondir(montant_de_deduction('part_time', date_debut_periode, date_fin_periode), 0.01)
if montant_mi_temps:
    montant_mi_temps_total = arrondir(montant_mi_temps * ((date_fin_periode - date_debut_periode).days + 1), 0.01)
    salaire_de_base = arrondir(salaire_de_base / 2, 0.01)
    description += 'Versement employeur - Mi temps thérapeutique: %s€ (montant journalier: %s€)\n\n' % (montant_mi_temps_total, montant_mi_temps)
    description += 'Salaire annuel réduit de moitié: %s€\n' % salaire_de_base

# Limiter à 100% du salaire de base
rente_SS = compl_rente_securite_sociale_annuelle()
description += 'Rente Sécurité Sociale: %s€\n' % compl_rente_securite_sociale_annuelle()
salaire_reference = tranches['TA'] + tranches['TB'] + tranches['TC']
if salaire_reference < salaire_de_base + rente_SS + montant_mi_temps and not compl_rente_annuelle_corrigee():
    salaire_annuel_base = arrondir(salaire_reference, 0.01) - rente_SS - montant_mi_temps
    description += 'Limitation à 100 pourcent du salaire soit %s€ %s\n' % (max(salaire_annuel_base, 0), salaire_de_base)
else:
    salaire_annuel_base = salaire_de_base - rente_SS
    description += "Salaire de base journalier déduit de la rente SS: %s€ - %s€ = %s€\n" % (salaire_de_base, rente_SS, salaire_annuel_base)
if salaire_annuel_base < 0:
    salaire_annuel_base = 0

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
periodes = periode_de_rente(date_debut_periode, date_fin_periode)
res = []

# Pas d'indémnisation si rente SS nulle
if not rente_SS:
    salaire_de_base = 0
    description = "Aucune prestation à verser car la rente de la sécurité sociale est nulle\n"  
    
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
