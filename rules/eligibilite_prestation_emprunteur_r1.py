# ---
# Name: Eligibilité emprunteur R1
# Short Name: eligibilite_prestation_emprunteur_r1
# Type: benefit
# ---

# DEBUT EL EMP R1 #
###################

######################
# DEBUT EL EMP R2 R3 #
######################


def gestion_delai_declaration_als():
    # gestion du délai de déclaration
    date_declaration = date_declaration_sinistre()
    fin_franchise = date_fin_franchise() or date_de_debut_du_prejudice()
    date_debut_prejudice = date_de_debut_du_prejudice()
    definition = compl_delai_de_declaration_definition()
    date_max_declaration = ajouter_jours(date_debut_prejudice, 1)

    if definition == 'jour_apres_arret_travail':
        date_max_declaration = ajouter_jours(
            date_debut_prejudice, compl_delai_de_declaration_quantite())
    elif definition == 'mois_apres_arret_travail':
        date_max_declaration = ajouter_mois(
            date_debut_prejudice, compl_delai_de_declaration_quantite())
    elif definition == 'jour_apres_franchise':
        date_max_declaration = ajouter_jours(
            fin_franchise, compl_delai_de_declaration_quantite())
    elif definition == 'mois_apres_franchise':
        date_max_declaration = ajouter_mois(
            fin_franchise, compl_delai_de_declaration_quantite())
    if date_max_declaration < date_declaration:
        if 'accord_de_prise_en_charge' not in documents_recus():
            ajouter_info(
                'La date de déclaration saisie %s est superieure à la date '
                'maximale de déclaration %s. Un accord de prise en charge est '
                'nécessaire pour continuer.' % (
                    formater_date(date_declaration),
                    formater_date(date_max_declaration)
                )
            )
            return False
    return True

#################
# FIN EL EMP R1 #
# DEBUT EL EMP R1 #
###################

######################
# DEBUT EL EMP R2 R3 #
######################


def gestion_categorie_rente(categories_autorisees):

    categorie = compl_categorie_de_rente_d_invalidite()

    if categorie is None:
        ajouter_info('Catégorie de rente non saisie.')
        return False

    if categorie in categories_autorisees:
        ajouter_info('Catégorie %s valide pour cette prestation' % categorie)
        return True

    ajouter_info('Catégorie %s invalide pour cette prestation' % categorie)
    return False


def eligibilite_emprunteur_r1():

    test_delai_declaration = gestion_delai_declaration_als()
    if not test_delai_declaration:
        return test_delai_declaration

    test_categorie_rente = gestion_categorie_rente(['r1'])
    return test_categorie_rente

return eligibilite_emprunteur_r1() # DECOMMENTER EL EMP R1

#################
# FIN EL EMP R1 #
