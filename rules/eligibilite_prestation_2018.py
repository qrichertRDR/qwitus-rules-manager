# ---
# Name: Eligibilité prestation (nouveau)
# Short Name: eligibilite_prestation_2018
# Type: benefit
# ---

###############
# ELIGIBILITE #
###############
def eligibilite_prestation(debut_arret_travail,
                           fin_franchise,
                           declaration_definition,
                           declaration_quantite,
                           rechute_definition,
                           rechute_quantite):
    description = u"ELIGIBILITE PRESTATION\n"

    if service_deductible():
        ajouter_info(u'La prestation est dans la période de franchise cumulée')
        return True

    description += u"\tPrestation hors de la période de franchise cumulée\n"

    # DELAI DE DECLARATION
    date_declaration = date_declaration_sinistre()

    date_max_declaration = ajouter_jours(debut_arret_travail, 1)
    if declaration_definition == 'jour_apres_arret_travail':
        date_max_declaration = ajouter_jours(debut_arret_travail, declaration_quantite)
    elif declaration_definition == 'mois_apres_arret_travail':
        date_max_declaration = ajouter_mois(debut_arret_travail, declaration_quantite)
    elif declaration_definition == 'jour_apres_franchise':
        date_max_declaration = ajouter_jours(fin_franchise, declaration_quantite)
    elif declaration_definition == 'mois_apres_franchise':
        date_max_declaration = ajouter_mois(fin_franchise, declaration_quantite)
    if date_max_declaration < date_declaration:
        if 'accord_de_prise_en_charge' not in documents_recus():
            ajouter_info(u'La date de déclaration saisie %s est superieure à la date maximale de déclaration %s. '
                         u'Un accord de prise en charge est nécessaire pour continuer.' % (
                             formater_date(date_declaration), formater_date(date_max_declaration)))
            return False

    description += u"\tDélai de déclaration (ok) : %s (déclaration) < %s (déclaration max)\n" % (
    formater_date(date_declaration), formater_date(date_max_declaration))

    # DELAI DE RECHUTE
    if est_une_rechute():
        date_max_rechute = date_fin_dernier_prejudice()

        if rechute_definition == 'mois':
            date_max_rechute = ajouter_mois(date_max_rechute, rechute_quantite)
        else:
            date_max_rechute = ajouter_jours(date_max_rechute, rechute_quantite)
        debut_prejudice = date_de_debut_du_prejudice()
        if debut_prejudice > date_max_rechute:
            if 'accord_de_prise_en_charge' not in documents_recus():
                ajouter_info(u'Pour une rechute, le nouvel arret doit survenir avant le %s.'
                             u'Un accord de prise en charge est nécessaire pour continuer'
                             u' ou vous pouvez créer un nouveau dossier de prestations' %
                             formater_date(date_max_rechute))
                return False

        description += u"\tDélai de rechute ok : %s (début préjudice) < %s (rechute max)\n" % \
                       (formater_date(debut_prejudice), formater_date(date_max_rechute))

    message_debug(description)
    return True


def el_eligibilite_prestation():
    description = u"EL ELIGIBILITE PRESTATION\n"

    utilisation_pivot = compl_1_delai_declaration_variable()
    fin_franchise = date_fin_franchise()
    if fin_franchise is None:
        message_absence = u"Date d'effet d'indemnisation introuvable."
        ajouter_info(message_absence)
        ajouter_avertissement(message_absence)
        ajouter_erreur(message_absence)
        return False

    rechute_quantite = compl_0_delai_rechute()
    rechute_definition = compl_0_delai_rechute_definition()

    description += u"\tDélai de rechute : %s %s\n" % (rechute_quantite, rechute_definition)

    # PIVOT
    debut_arret_travail = date_de_debut_du_prejudice()
    if utilisation_pivot == 'oui':
        valeur_duree = compl_2_valeur_pivot()
        type_duree = compl_3_type_pivot()

        delta_duree = relativedelta(days=+0)
        if type_duree == "jour":
            delta_duree = relativedelta(days=+valeur_duree)
        elif type_duree == "mois":
            delta_duree = relativedelta(months=+valeur_duree)

        delta_franchise = fin_franchise - debut_arret_travail
        if delta_franchise.days < delta_duree.days:
            declaration_quantite = compl_4_delai_declaration_avant_pivot()
            declaration_definition = compl_5_delai_declaration_avant_pivot_definition()
        else:
            declaration_quantite = compl_6_delai_declaration_apres_pivot()
            declaration_definition = compl_7_delai_declaration_apres_pivot_definition()

    else:
        declaration_quantite = compl_2_delai_declaration()
        declaration_definition = compl_3_delai_declaration_definition()

    description += u"\tUtlisation pivot ? %s\n" % utilisation_pivot
    description += u"\tFin franchise : %s\n" % formater_date(fin_franchise)
    description += u"\tDebut arret travail : %s\n" % formater_date(debut_arret_travail)
    description += u"\tDélai de déclaration : %s %s\n" % (declaration_quantite, declaration_definition)
    message_debug(description)

    return eligibilite_prestation(debut_arret_travail,
                                  fin_franchise,
                                  declaration_definition,
                                  declaration_quantite,
                                  rechute_definition,
                                  rechute_quantite)


# DECOMMENTER SOUS COOG
return el_eligibilite_prestation()
