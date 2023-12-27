# ---
# Name: Rente basée sur la catégorie
# Short Name: rente_abse_sur_la_categorie
# Type: benefit
# ---

categorie = compl_categorie_de_rente_d_invalidite()
rente_SS = compl_rente_securite_sociale_annuelle()
description = ''

if categorie == 'cat_rente_inva_1':
    tauxTA = param_1_pourcentage_ta_1ere_categorie()
    tauxTB = param_2_pourcentage_tb_1ere_categorie()
    tauxTC = param_3_pourcentage_tc_1ere_categorie()
elif categorie == 'cat_rente_inva_2':
    tauxTA = param_4_pourcentage_ta_2eme_categorie()
    tauxTB = param_5_pourcentage_tb_2eme_categorie()
    tauxTC = param_6_pourcentage_tc_2eme_categorie()
elif categorie == 'cat_rente_inva_3':
    tauxTA = param_7_pourcentage_ta_3eme_categorie()
    tauxTB = param_8_pourcentage_tb_3eme_categorie()
    tauxTC = param_9_pourcentage_tc_3eme_categorie()

tranches = tranche_salaire(['gross_salary'])
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

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
periodes = periode_de_rente(date_debut_periode, date_fin_periode)
res = []

if compl_rente_annuelle_corrigee():
    salaire_de_base = compl_rente_annuelle_corrigee()

# Pas d'indémnisation si rente SS nulle
if not rente_SS:
    salaire_de_base = 0
    description = "Aucune prestation à verser car la rente de la sécurité sociale est nulle\n"  

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
    if montant_reference < arrondir(montant_proratise, 0.01) + arrondir(rente_SS_reference, 0.01) + montant_mi_temps_total and not compl_rente_annuelle_corrigee():
        montant_proratise_deduit = arrondir(montant_proratise, 0.01) - arrondir(rente_SS_reference, 0.01) - montant_mi_temps_total
        montant_par_unite = arrondir(montant_par_unite, 0.01) - arrondir(rente_SS_unite, 0.01) - montant_mi_temps_total
        description += 'Limitation à 100 pourcent du salaire soit %s€ %s\n' % (max(montant_proratise_deduit, 0), montant_reference)
    else:
        montant_proratise_deduit = montant_proratise - arrondir(rente_SS_reference, 0.01)
        montant_par_unite = montant_par_unite - arrondir(rente_SS_unite, 0.01)
        description += "Montant proratisé déduit de la rente SS: %s€ - %s€ = %s€\n" % (montant_proratise, rente_SS_reference, montant_proratise_deduit)
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
