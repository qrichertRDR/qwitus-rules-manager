# ---
# Name: Traitement rente invalidité par tranche de salaire (par catégorie et par taux)
# Short Name: coog_traitement_rente_invalidite_par_tranche_salaire_categorie_taux
# Type: benefit
# ---

rente_SS = compl_rente_securite_sociale_periode()
traitement_de_reference = param_0_traitement_de_reference()
categorie = compl_categorie_de_rente_d_invalidite()
taux_incapacite_permanente = compl_taux_incapacite_permanente()

if traitement_de_reference == 'salaire_brut':
    tranches = tranche_salaire(['gross_salary'])
elif traitement_de_reference == 'salaire_net':
    tranches = tranche_salaire(['net_salary'])
elif traitement_de_reference == 'salaire_brut_prime':
    tranches = tranche_salaire(['gross_salary', 'salary_bonus'])
elif traitement_de_reference == 'salaire_net_prime':
    tranches = tranche_salaire(['net_salary', 'net_salary_bonus'])

salaire_de_reference = 0 
rente_de_base = 0
description = u''
annex_rule_code = 'coog_prestations_annexes_rente'
trancheTA, trancheTB, trancheTC = 0, 0, 0
date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()

if not rente_SS:
    rente_de_base = 0
    description = u'Aucune prestation a verser car la rente de la securite sociale est nulle\n'

pourcentage_ta_r1 = param_1_pourcentage_ta_r1()
pourcentage_tb_r1 = param_2_pourcentage_tb_r1()
pourcentage_tc_r1 = param_3_pourcentage_tc_r1()
pourcentage_ta_r2 = param_4_pourcentage_ta_r2()
pourcentage_tb_r2 = param_5_pourcentage_tb_r2()
pourcentage_tc_r2 = param_6_pourcentage_tc_r2()
pourcentage_ta_r3 = param_7_pourcentage_ta_r3()
pourcentage_tb_r3 = param_8_pourcentage_tb_r3()
pourcentage_tc_r3 = param_9_pourcentage_tc_r3()

taux_tranches = rule_calcul_taux(categorie=categorie, pourcentage_ta_r1=pourcentage_ta_r1, pourcentage_tb_r1=pourcentage_tb_r1, pourcentage_tc_r1=pourcentage_tc_r1, pourcentage_ta_r2=pourcentage_ta_r2, pourcentage_tb_r2=pourcentage_tb_r2, pourcentage_tc_r2=pourcentage_tc_r2, pourcentage_ta_r3=pourcentage_ta_r3, pourcentage_tb_r3=pourcentage_tb_r3, pourcentage_tc_r3=pourcentage_tc_r3, taux_incapacite_permanente=taux_incapacite_permanente)
if len(taux_tranches) != 1:
    ajouter_erreur('Taux tranches invalide')
tauxTA = taux_tranches[0]['tauxTA']
tauxTB = taux_tranches[0]['tauxTB']
tauxTC = taux_tranches[0]['tauxTC']
TA = tranches['TA']
TB = tranches['TB']
TC = tranches['TC']

salaires = rule_calcul_tranches(description=description, ta=TA, tb=TB, tc=TC, salaire_de_reference=salaire_de_reference, rente_ss=rente_SS, rente_de_base=rente_de_base, tauxTA=tauxTA, tauxTB=tauxTB, tauxTC=tauxTC,
taux_incapacite_permanente=taux_incapacite_permanente, categorie=categorie)
assert len(salaires) == 1
trancheTA = salaires[0]['trancheTA']
trancheTB = salaires[0]['trancheTB']
trancheTC = salaires[0]['trancheTC']
salaire_de_reference = salaires[0]['salaire_de_reference']
rente_de_base = salaires[0]['rente_de_base']
description = salaires[0]['description']

periodes = periode_de_rente(date_debut_periode, date_fin_periode)
annuites = calcul_annuites(periods=periodes, description=description, annuity_amount=rente_de_base, ss_annuity_amount=rente_SS, reference_salary=salaire_de_reference, trancheTA=trancheTA, trancheTB=trancheTB, trancheTC=trancheTC, annex_rule_code=annex_rule_code)
return annuites
