# ---
# Name: Salaire net par tranche de salaire par catégories avec rupture Rente
# Short Name: SN_rente_rupture
# Type: benefit
# ---

categorie = compl_categorie_de_rente_d_invalidite()
r1_as_r2 = param_4_pourcentage_r1_defini_comme_pourcentage_de_r2_SN()
rupture = element_couvert_est_beneficiaire()

if categorie == 'r1':
    tauxTA = param_1_pourcentage_ta_r1_SN() 
    tauxTB = param_1_pourcentage_tb_r1_SN()
    tauxTC = param_1_pourcentage_tc_r1_SN()
    TA_rupture, TB_rupture, TC_rupture = param_5_ta_tb_tc_de_r1_rupture().split(',')
    TA_rupture, TB_rupture, TC_rupture = (Decimal(TA_rupture), Decimal(TB_rupture), Decimal(TC_rupture))
elif categorie == 'r2':
    tauxTA = param_2_pourcentage_ta_r2_SN()
    tauxTB = param_2_pourcentage_tb_r2_SN()
    tauxTC = param_2_pourcentage_tc_r2_SN()
    TA_rupture, TB_rupture, TC_rupture = param_5_ta_tb_tc_de_r2_rupture().split(',')
    TA_rupture, TB_rupture, TC_rupture = (Decimal(TA_rupture), Decimal(TB_rupture), Decimal(TC_rupture))
elif categorie == 'r3':
    tauxTA = param_3_pourcentage_ta_r3_SN()
    tauxTB = param_3_pourcentage_tb_r3_SN()
    tauxTC = param_3_pourcentage_tc_r3_SN()
    TA_rupture, TB_rupture, TC_rupture = param_5_ta_tb_tc_de_r3_rupture().split(',')
    TA_rupture, TB_rupture, TC_rupture = (Decimal(TA_rupture), Decimal(TB_rupture), Decimal(TC_rupture))

if r1_as_r2 and categorie == 'r1' and not rupture:
    tauxTA = (tauxTA * param_2_pourcentage_ta_r2_SN()) / 100
    tauxTB = (tauxTB * param_2_pourcentage_tb_r2_SN()) / 100
    tauxTC = (tauxTC * param_2_pourcentage_tc_r2_SN()) / 100

if rupture:
    tauxTA, tauxTB, tauxTC = (TA_rupture, TB_rupture, TC_rupture)
    if r1_as_r2 and categorie == 'r1':
        TA_rupture_r2, TB_rupture_r2, TC_rupture_r2 = param_5_ta_tb_tc_de_r2_rupture().split(',')
        TA_rupture_r2, TB_rupture_r2, TC_rupture_r2  = (Decimal(TA_rupture_r2), Decimal(TB_rupture_r2), Decimal(TC_rupture_r2))       
        tauxTA = (tauxTA * TA_rupture_r2) / 100
        tauxTB = (tauxTB * TB_rupture_r2) / 100
        tauxTC = (tauxTC * TC_rupture_r2) / 100
        
return rule_SN_rente_global(taux_a=tauxTA, taux_b=tauxTB, taux_c=tauxTC, rente_securite_sociale_annuelle=compl_rente_securite_sociale_annuelle())
