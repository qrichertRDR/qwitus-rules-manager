# ---
# Name: Salaire brut par tranche de salaire rente
# Short Name: SB_rente
# Type: benefit
# ---

rente_SS = compl_rente_securite_sociale_annuelle()
tranches = tranche_salaire(['gross_salary', 'salary_bonus'])
tranches_net = tranche_salaire(['net_salary'])
categorie = compl_categorie_de_rente_d_invalidite()
taux_incapacite_permanente = compl_taux_incapacite_permanente()
salaire_de_reference = 0
salaire_de_reference_net = 0
rente_de_base = 0
description = ''
trancheTA, trancheTB, trancheTC = 0, 0, 0
r1_as_r2 = param_4_pourcentage_r1_defini_comme_pourcentage_de_r2()
date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()

# Pas d'indémnisation si rente SS nulle
if not rente_SS:
    rente_de_base = 0
    description = "Aucune prestation à verser car la rente de la securité sociale est nulle\n"  

# calcul de la rente annuelle
if categorie == 'r1' and not r1_as_r2:
    tauxTA = param_1_pourcentage_ta_r1()
    tauxTB = param_1_pourcentage_tb_r1()
    tauxTC = param_1_pourcentage_tc_r1()
elif categorie == 'r2' or categorie == 'r1' and r1_as_r2:
    tauxTA = param_2_pourcentage_ta_r2()
    tauxTB = param_2_pourcentage_tb_r2()
    tauxTC = param_2_pourcentage_tc_r2()
elif categorie == 'r3':
    tauxTA = param_3_pourcentage_ta_r3()
    tauxTB = param_3_pourcentage_tb_r3()
    tauxTC = param_3_pourcentage_tc_r3()

# Rajout pour RAT 19/10/2017 - GGA 
elif categorie == 'rat':
    if taux_incapacite_permanente >= 66:
        tauxTA = param_2_pourcentage_ta_r2()
        tauxTB = param_2_pourcentage_tb_r2()
        tauxTC = param_2_pourcentage_tc_r2()
    elif taux_incapacite_permanente >= 33 and taux_incapacite_permanente <= 66:
        coefficient = taux_incapacite_permanente/66
        #Rajout arrondir 25/10/2017 - GGA/CRU
        tauxTA = param_2_pourcentage_ta_r2()
        tauxTB = param_2_pourcentage_tb_r2()
        tauxTC = param_2_pourcentage_tc_r2()
    elif taux_incapacite_permanente < 33:
        tauxTA = 0
        tauxTB = 0
        tauxTC = 0
else:
    ajouter_erreur("La catégorie est invalide")

trancheTA, trancheTB, trancheTC = 0, 0, 0
if tauxTA:
    trancheTA = arrondir(tauxTA * tranches['TA'] / 100.0, 0.01)
    salaire_de_reference += tranches['TA']
    salaire_de_reference_net += tranches_net['TA']
    rente_de_base += trancheTA
    description += 'Salaire de base (TA): %s%% * %s€ = %s€\n' % (tauxTA, tranches['TA'], trancheTA)
if tauxTB:
    trancheTB = arrondir(tauxTB * tranches['TB'] / 100.0, 0.01)
    salaire_de_reference += tranches['TB']
    salaire_de_reference_net += tranches_net['TB']
    rente_de_base += trancheTB
    description += 'Salaire de base (TB): %s%% * %s€ = %s€\n' % (tauxTB, tranches['TB'], trancheTB)
if tauxTC:
    trancheTC = arrondir(tauxTC * tranches['TC'] / 100.0, 0.01)
    salaire_de_reference += tranches['TC']
    salaire_de_reference_net += tranches_net['TC']
    rente_de_base += trancheTC
    description += 'Salaire de base (TC): %s%% * %s€ = %s€\n' % (tauxTC, tranches['TC'], trancheTC)

salaire_de_reference = arrondir(salaire_de_reference, 0.01)
salaire_de_reference_net = arrondir(salaire_de_reference_net, 0.01)
rente_de_base = arrondir(rente_de_base, 0.01)

# deduction de la rente
if r1_as_r2 and categorie == 'r1':
    rente_SS_r2 = arrondir(rente_SS * 50 / 30, 0.01)
    rente_de_base -= rente_SS_r2
    tauxTA_r1 = param_1_pourcentage_ta_r1()
    rente_de_base = arrondir(rente_de_base * tauxTA_r1 /100, 0.01) 
else:
    description += 'Rente Sécurité Sociale: %s€\n' % rente_SS
    rente_de_base -= rente_SS

if compl_rente_annuelle_corrigee():
    rente_de_base = compl_rente_annuelle_corrigee()
description += 'Rente de base à %s€\n' % rente_de_base

if categorie == 'rat':
    description +='Taux Incapacité : %s%%\n' % (taux_incapacite_permanente)
    description += 'Rente de base - détail du calcul :  %s€=(%s-%s)*%s%%\n' % (rente_de_base,salaire_de_reference,rente_SS,taux_incapacite_permanente)
else:
    description += 'Rente de base - détail du calcul :  %s€=(%s-%s)\n' % (rente_de_base,salaire_de_reference,rente_SS)

# calcul des sous périodes
periodes = periode_de_rente(date_debut_periode, date_fin_periode)
res = []

description_copy = description
for date_debut, date_fin, periode_entiere, prorata, unit in periodes:
    description = description_copy
    if not periode_entiere:
        ratio = 365
    else:
        ratio = 12

    rente_de_base_periode = arrondir(rente_de_base / ratio * prorata, 0.01)
    salaire_de_reference_periode = arrondir(salaire_de_reference / ratio * prorata, 0.01)
    salaire_de_reference_net_periode = arrondir(salaire_de_reference_net / ratio * prorata, 0.01)
    rente_SS_periode = arrondir(rente_SS / ratio * prorata, 0.01)
    if rente_de_base_periode < 0:
        rente_de_base_periode = 0
        
    # calcul de la limite
    type_de_regle='taux_activite'
    if compl_ancienne_regle_TP_allianz():
        type_de_regle = 'ancienne_regle_allianz'
    rente_de_base_periode, annexe_description = rule_prestations_annexes_rente(
        type_de_regle=type_de_regle, date_debut_periode=date_debut, date_fin_periode=date_fin, 
        rente_de_base=rente_de_base_periode, salaire_de_reference=salaire_de_reference_periode, rente_SS=rente_SS_periode,
        rente_ss_reellement_percue=compl_rente_SS_percue_prestations_annexes(), salaire_de_reference_net=salaire_de_reference_net_periode) 
    description += annexe_description

    if taux_incapacite_permanente >= 33 and taux_incapacite_permanente <= 66 and not compl_rente_annuelle_corrigee():
        rente_de_base_periode = rente_de_base_periode * coefficient
#        rente_de_base_periode = rente_de_base_periode * taux_incapacite_permanente
    
    rente_de_base_unitaire = arrondir(rente_de_base_periode / prorata, 0.01)
    res.append({
                'start_date': date_debut,
                'end_date': date_fin,
                'nb_of_unit': prorata,
                'unit': unit,
                'amount': rente_de_base_periode,
                'base_amount': rente_de_base_unitaire,
                'amount_per_unit': rente_de_base_unitaire,
                'description': description,
                'extra_details': {
                    'tranche_a': str(trancheTA),
                    'tranche_b': str(trancheTB),
                    'tranche_c': str(trancheTC),
                    }
                })
return res
