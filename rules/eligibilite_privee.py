# ---
# Name: Eligibilité (privée)
# Short Name: eligibilite_privee
# Type: tool
# ---

# DEBUT EL #
############

def rule_eligibilite_privee():

    res, information, avertissement, erreur = \
        True, \
        '', \
        '', \
        ''

    description = 'ELIGIBILITE PRESTATION\n'

    date_fin_franchise_initiale = date_fin_franchise()

    # PARAMETRE MANQUANT
    date_retour_dei_param_manquant = datetime.date(9999, 1, 1)

    if date_fin_franchise_initiale == date_retour_dei_param_manquant:
        res = False
        information = 'Paramètre manquant sur la franchise.'
        ajouter_info(information)
        return res, information, avertissement, erreur

    # DEI MANUELLE MANQUANTE
    date_retour_dei_non_saisie_autre = datetime.date(9999, 1, 3)
    date_retour_dei_non_saisie_recccn = datetime.date(9999, 1, 4)
    date_retour_dei_non_saisie_relccn = datetime.date(9999, 1, 5)
    date_retour_dei_non_saisie_cumulee_annee_civile = datetime.date(9999, 1, 6)
    date_retour_dei_non_saisie_cumulee_annee_glissante = datetime.date(9999, 1, 7)

    type_dei = ''
    if date_fin_franchise_initiale == date_retour_dei_non_saisie_autre:
        type_dei = 'autre'
    elif date_fin_franchise_initiale == date_retour_dei_non_saisie_recccn:
        type_dei = 'relais complément ccn'
    elif date_fin_franchise_initiale == date_retour_dei_non_saisie_relccn:
        type_dei = 'relais ccn'
    elif date_fin_franchise_initiale == date_retour_dei_non_saisie_cumulee_annee_civile:
        type_dei = 'cumulée année civile'
    elif date_fin_franchise_initiale == date_retour_dei_non_saisie_cumulee_annee_glissante:
        type_dei = 'cumulée année glissante'

    if date_retour_dei_non_saisie_autre <= date_fin_franchise_initiale <= date_retour_dei_non_saisie_cumulee_annee_glissante:
        res = False
        information = "Absence de date d'effet d'indemnisation %s." % type_dei
        ajouter_info(information)
        return res, information, avertissement, erreur

    if service_deductible():
        res = True
        information = 'La prestation est dans la période de franchise cumulée'
        ajouter_info(information)
        return res, information, avertissement, erreur

    description += '\tPrestation hors de la période de franchise cumulée\n'

    ########################
    # DELAI DE DECLARATION #
    ########################
    res, date_decla, date_decla_max, delta_decla, information, avertissement, erreur, desc_delai_decla = rule_gestion_delai_declaration(
        date_fin_franchise_initiale=date_fin_franchise_initiale)

    if not res:
        message_debug(desc_delai_decla)
        if information != '':
            ajouter_info(information)
        if avertissement != '':
            ajouter_avertissement(avertissement)
        if erreur != '':
            ajouter_avertissement(erreur)
        return res, information, avertissement, erreur

    ####################
    # DELAI DE RECHUTE #
    ####################

    res, information, avertissement, erreur, desc_rechute = rule_gestion_delai_rechute()
    if not res:
        message_debug(desc_rechute)
        if information != '':
            ajouter_info(information)
        if avertissement != '':
            ajouter_avertissement(avertissement)
        if erreur != '':
            ajouter_avertissement(erreur)
        return res, information, avertissement, erreur

    return res, information, avertissement, erreur

return rule_eligibilite_privee() # DECOMMENTER SOUS COOG

##########
# FIN EL #
