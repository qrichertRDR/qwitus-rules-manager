# ---
# Name: Règle analyse médicale GAN
# Short Name: regle_analyse_medicale_gan
# Type: underwriting_type
# ---

date = date_fin_franchise()
#On bloque à partir du 31 jours après la franchise 
date = ajouter_jours(date, 31)
if code_de_l_evenement_du_prejudice() == 'maternite':
    return None, None
return 'analyse_medicale_allianz', date
