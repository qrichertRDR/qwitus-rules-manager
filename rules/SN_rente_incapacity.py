# ---
# Name: Salaire net par tranche de salaire avec incapacité ou invalidité Rente
# Short Name: SN_rente_incapacity
# Type: benefit
# ---

categorie = compl_categorie_de_rente_d_invalidite()
evenement = code_de_l_evenement_du_prejudice()
in_activity = (compl_activite_du_sinistre() == '1_in_activity')
incapacity_rate = compl_taux_d_incapacite()


# Incapacity
if 'travail' in evenement:
    
    if incapacity_rate >= 33 and incapacity_rate < 66:
        if in_activity:
            TA = TB = ((3 * incapacity_rate) / 2 * param_4_pourcentage_taux_d_incapacite_entre_33_et_66_en_activite())
        else:
            TA = TB = ((3 * incapacity_rate) / 2 * param_5_pourcentage_taux_d_incapacite_entre_33_et_66_sans_activite())
    else:
        # Si > 66: = deuxieme ou troisieme catégorie
        TA = TB = param_3_pourcentage_invalidite_ta_et_tb_r2_et_r3()
# Disability
else:
    if categorie == 'r1':
        if in_activity:
            TA  = TB = param_2_pourcentage_invalidite_ta_et_tb_r1_en_activite()
        else:
            TA = TB = param_1_pourcentage_invalidite_ta_et_tb_r1_sans_activite()
    elif categorie in ('r2', 'r3'):
        TA = TB = param_3_pourcentage_invalidite_ta_et_tb_r2_et_r3()

TC = 0

# Return the Global SN_Rente rule calculation with updated rates
return rule_SN_rente_global(taux_a=TA, taux_b=TB, taux_c=TC, rente_securite_sociale_annuelle=compl_rente_securite_sociale_annuelle())
