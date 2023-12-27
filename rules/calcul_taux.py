# ---
# Name: Calcul Taux
# Short Name: calcul_taux
# Type: benefit
# ---

categorie = param_categorie()
pourcentage_ta_r1=param_pourcentage_ta_r1()
pourcentage_tb_r1=param_pourcentage_tb_r1()
pourcentage_tc_r1=param_pourcentage_tc_r1()
pourcentage_ta_r2=param_pourcentage_ta_r2()
pourcentage_tb_r2=param_pourcentage_tb_r2()
pourcentage_tc_r2=param_pourcentage_tc_r2()
pourcentage_ta_r3=param_pourcentage_ta_r3()
pourcentage_tb_r3=param_pourcentage_tb_r3()
pourcentage_tc_r3=param_pourcentage_tc_r3()
taux_incapacite_permanente=param_taux_incapacite_permanente()

tauxTA = 0
tauxTB = 0
tauxTC = 0

if categorie == 'r1':
    tauxTA = pourcentage_ta_r1
    tauxTB = pourcentage_tb_r1
    tauxTC = pourcentage_tc_r1
elif categorie == 'r2':
    tauxTA = pourcentage_ta_r2
    tauxTB = pourcentage_tb_r2
    tauxTC = pourcentage_tc_r2
elif categorie == 'r3':
    tauxTA = pourcentage_ta_r3
    tauxTB = pourcentage_tb_r3
    tauxTC = pourcentage_tc_r3

elif categorie =='rat':
    if taux_incapacite_permanente >= 66:
        tauxTA = pourcentage_ta_r3
        tauxTB = pourcentage_tb_r3
        tauxTC = pourcentage_tc_r3
    elif taux_incapacite_permanente >= 33 and taux_incapacite_permanente <= 66:
        tauxTA = (Decimal('3') / Decimal('2')) * (taux_incapacite_permanente / 100) * pourcentage_ta_r2 
        tauxTB = (Decimal('3') / Decimal('2')) * (taux_incapacite_permanente / 100) * pourcentage_tb_r2
        tauxTC = (Decimal('3') / Decimal('2')) * (taux_incapacite_permanente / 100) * pourcentage_tc_r2
    elif taux_incapacite_permanente < 33:
        tauxTA = 0
        tauxTB = 0
        tauxTC = 0

return [{'tauxTA': tauxTA,
    'tauxTB': tauxTB,
    'tauxTC': tauxTC
    }]
