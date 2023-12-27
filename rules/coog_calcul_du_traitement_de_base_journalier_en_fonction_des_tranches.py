# ---
# Name: Calcul du traitement de base  journalier en fonction des tranches
# Short Name: coog_calcul_du_traitement_de_base_journalier_en_fonction_des_tranches
# Type: benefit
# ---

description = ''
calcul_salaire = param_methode_de_traitement_de_reference()
donnees_salaire = ['gross_salary' if 'brut' in calcul_salaire else 'net_salary']
if 'prime' in calcul_salaire:
    if 'brut' in calcul_salaire:
        donnees_salaire.append('salary_bonus')
    else:
        donnees_salaire.append('net_salary_bonus')
tranches = tranche_salaire(donnees_salaire)

tranches['TA'] = arrondir(tranches['TA'], 0.01)
tranches['TB'] = arrondir(tranches['TB'], 0.01)
tranches['TC'] = arrondir(tranches['TC'], 0.01)

traitement_de_reference = tranches['TA'] + tranches['TB'] + tranches['TC']
traitement_de_base = 0
trancheTA, trancheTB, trancheTC = 0, 0, 0
pourcentage_TA = param_pourcentage_ij_ta()
pourcentage_TB = param_pourcentage_ij_tb()
pourcentage_TC = param_pourcentage_ij_tc()
if pourcentage_TA:
    trancheTA = arrondir(pourcentage_TA * tranches['TA'] / 100.0, 0.01)
    traitement_de_base += trancheTA
    description += 'Traitement de base (TA): %s * %s /100 = %s€\n' % (pourcentage_TA, tranches['TA'], trancheTA)
if pourcentage_TB:
    trancheTB = arrondir(pourcentage_TB * tranches['TB'] / 100.0, 0.01)
    traitement_de_base += trancheTB
    description += 'Traitement de base (TB): %s * %s /100 = %s€\n' % (pourcentage_TB, tranches['TB'], trancheTB)
if pourcentage_TC:
    trancheTC = arrondir(pourcentage_TC * tranches['TC'] / 100.0, 0.01)
    traitement_de_base += trancheTC
    description += 'Traitement de base (TC): %s * %s /100 = %s€\n' % (pourcentage_TC, tranches['TC'], trancheTC)
description += 'Traitement de base: %s\n' % traitement_de_base
traitement_journalier = arrondir(traitement_de_base / 365, 0.01)

description += 'Traitement de base journalier: %s / 365 = %s€\n\n' % (traitement_de_base, traitement_journalier)
return traitement_journalier, traitement_de_reference, trancheTA, trancheTB, trancheTC, description
