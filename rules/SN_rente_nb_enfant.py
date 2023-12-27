# ---
# Name: Salaire net par tranche de salaire par catégories et selon nb enfant a charge Rente
# Short Name: SN_rente_nb_enfant
# Type: benefit
# ---

categorie = compl_categorie_de_rente_d_invalidite()
r1_as_r2 = param_4_pourcentage_r1_defini_comme_pourcentage_de_r2_SN()
nb_enfant_a_charge = compl_nombre_d_enfants_a_charge()
donnee = {
    'r1': param_1_R1(),
    'r2': param_2_R2(),
    'r3': param_3_R3(),
    }.get(categorie)
taux_par_enfant = rule_transformation_des_parametres_indemnistation_rente(donnee=donnee)
if taux_par_enfant is None:
      ajouter_erreur('La catégorie n\'est pas valide (%s).' % categorie)
for enfants, taux in taux_par_enfant.iteritems():
    if nb_enfant_a_charge >= enfants[0] and nb_enfant_a_charge <= enfants[1]:
        tauxTA, tauxTB, tauxTC = taux
        break

if r1_as_r2 and categorie == 'r1':
    taux_r2_par_enfant = rule_transformation_des_parametres_indemnistation_rente(donnee=param_2_R2())
    for enfants, taux in taux_r2_par_enfant.iteritems():
        if nb_enfant_a_charge >= enfants[0] and nb_enfant_a_charge <= enfants[1]:
            tauxTAR2, tauxTBR2, tauxTCR2 = taux
            break
    tauxTA = (tauxTA * tauxTAR2) / 100
    tauxTB = (tauxTB * tauxTBR2) / 100
    tauxTC = (tauxTC * tauxTCR2) / 100

return rule_SN_rente_global(taux_a=tauxTA, taux_b=tauxTB, taux_c=tauxTC,
    rente_securite_sociale_annuelle=compl_rente_securite_sociale_annuelle())
