# ---
# Name: Franchise cumulée conditionnelle (sauvegarde recette24_2022_08_11)
# Short Name: fr_cumul_cond
# Type: benefit_deductible
# ---

# DEBUT FR JOURS ARRET #
########################

def fr_jours_arret():

    date_erreur = datetime.date(9999, 1, 1)

    dateanciennete = compl_dateanciennete()
    if (dateanciennete is None):
        return date_erreur

    anciennete = jours_entre(dateanciennete, date_de_debut_du_prejudice())/365
    delta_fr=0
    delta_fr2=0

    if anciennete<1:
        delta_fr = 4
        delta_fr2 = 3

    elif anciennete>=1 and anciennete<6:
        delta_fr=30
	    
    elif anciennete>=6 and anciennete<11:
        delta_fr=40

    elif anciennete>=11 and anciennete<16:
        delta_fr=50
	    
    elif anciennete>=16 and anciennete<21:
        delta_fr=60
	    
    elif anciennete>=21 and anciennete<26:
        delta_fr=70
	    
    elif anciennete>=26 and anciennete<31:
        delta_fr=80
	    
    elif anciennete>=31 and anciennete<46:
        delta_fr=90
        
    return rule_fr_jours_arret_standard(
        a1_type_franchise='continue',
        a2_franchise_accident=3+delta_fr,
        a2a_condition_accident='aucune',
        a2b_rachat_accident=None,
        a3_franchise_accident_travail=0+delta_fr+delta_fr2,
        a3a_condition_accident_travail='aucune',
        a3b_rachat_accident_travail=None,
        a4_franchise_maladie=3+delta_fr,
        a4a_condition_maladie='aucune',
        a4b_rachat_maladie=None,
        a5_franchise_maladie_professionnelle=0+delta_fr+delta_fr2,
        a5a_condition_maladie_professionnelle='aucune',
        a5b_rachat_maladie_professionnelle=None,
        a6_franchise_maternite=0+delta_fr+delta_fr2,
        a6a_condition_maternite='aucune',
        a6b_rachat_maternite=None
    )    


return fr_jours_arret() # DECOMMENTER SOUS COOG

######################
# FIN FR JOURS ARRET #
