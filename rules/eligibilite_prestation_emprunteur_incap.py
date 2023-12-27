# ---
# Name: Eligibilité emprunteur INCAP
# Short Name: eligibilite_prestation_emprunteur_incap
# Type: benefit
# ---

# DEBUT EL EMP INC #
####################

###################
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
#################

####################
# FIN EL EMP R2 R3 #
####################


def eligibilite_emprunteur_incap():

    test_delai_declaration = gestion_delai_declaration_als()
    if not test_delai_declaration:
        return test_delai_declaration

    # gestion de la rechute
    res, information, avertissement, erreur, desc_rechute = \
        rule_gestion_delai_rechute()

    if not res:
        message_debug(desc_rechute)
        if information != '':
            ajouter_info(information)

    return res

return eligibilite_emprunteur_incap() # DECOMMENTER EL EMP INC

##################
# FIN EL EMP INC #
