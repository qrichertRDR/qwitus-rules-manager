# ---
# Name: Gestion du délai de rechute (nouveau, prive)
# Short Name: gestion_delai_rechute
# Type: tool
# ---

# DEBUT GESTION DELAI RECHUTE #
###############################

def rule_gestion_delai_rechute():
    res, information, avertissement, erreur, description_rechute = \
        True, \
        '', \
        '', \
        '', \
        ''

    rechute_quantite = compl_1a_delai_rechute()
    rechute_definition = compl_1b_delai_rechute_definition()
    description_rechute = \
        '\tDélai de rechute : %s %s\n' % (
            rechute_quantite,
            rechute_definition
        )

    if est_une_rechute():
        date_max_rechute = date_fin_dernier_prejudice()
        if rechute_definition == 'mois':
            date_max_rechute = ajouter_mois(date_max_rechute, rechute_quantite)
        elif rechute_definition == 'jours':
            date_max_rechute = ajouter_jours(date_max_rechute, rechute_quantite)
        elif rechute_definition == 'sans_limite':
            date_max_rechute = datetime.date(9999,12,31)
        else:
            res = False
            information = 'Définition de rechute invalide: %s' % rechute_definition
            ajouter_info(information)
            return res, information, avertissement, erreur, description_rechute

        rechute_condition_cause = compl_1c_cause_rechute()
        debut_prejudice = date_de_debut_du_prejudice()

        # HORS DELAI DE RECHUTE
        if debut_prejudice > date_max_rechute:
            res = False
            information = 'Pour une rechute, le nouvel arret doit survenir avant le %s.' % formater_date(date_max_rechute)
            information += '\nSinon, vous pouvez créer un nouveau dossier de prestations.'
            ajouter_info(information)
            return res, information, avertissement, erreur, description_rechute
        # DELAI DE RECHUTE RESPECTE
        else:
            if rechute_condition_cause is not None and rechute_condition_cause == True:
                if 'accord_de_prise_en_charge_rechute_pour_meme_cause' not in documents_recus():
                    res = False
                    information = 'Pour une rechute, un accord de prise en charge de rechute pour même cause est nécessaire.'
                    information += '\nSinon, vous pouvez créer un nouveau dossier de prestations.'
                    ajouter_info(information)
                    return res, information, avertissement, erreur, description_rechute
            else:
                if 'accord_de_prise_en_charge_rechute' not in documents_recus():
                    res = False
                    information = 'Pour une rechute, un accord de prise en charge de rechute est nécessaire.'
                    information += '\nSinon, vous pouvez créer un nouveau dossier de prestations.'
                    ajouter_info(information)
                    return res, information, avertissement, erreur, description_rechute

        description_rechute += '\tDélai de rechute ok : %s (début préjudice) < %s (rechute max)\n' % \
                       (formater_date(debut_prejudice), formater_date(date_max_rechute))

    message_debug(description_rechute)
    return res, information, avertissement, erreur, description_rechute


def gestion_delai_rechute():
    return rule_gestion_delai_rechute()

return gestion_delai_rechute() # DECOMMENTER SOUS COOG

#############################
# FIN GESTION DELAI RECHUTE #
