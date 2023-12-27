# ---
# Name: Message d'erreur analyse de risque Allianz
# Short Name: message_d_erreur_analyse_de_risque_allianz
# Type: process_check
# ---

if compl_categorie_de_population() == 'TNS' or nombre_initial_de_sous_elements_couverts() <= 5:
    ajouter_avertissement(
        u'Merci de communiquer au médecin le questionnaire '
        u'de santé fourni à la souscription')
return
