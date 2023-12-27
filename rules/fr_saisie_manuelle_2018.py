# ---
# Name: Franchise avec saisie manuelle (nouveau)
# Short Name: fr_saisie_manuelle_2018
# Type: benefit_deductible
# ---

# DEBUT FR SAISIE MANUELLE #
############################
# TODO gestion déclaration tardive saisie manuelle

def fr_saisie_manuelle():
    """
    :return: date de début d'indemnisation saisie manuellement
    :rtype: datetime
    """

    # PARAMETRE
    type_franchise = param_type_franchise()
    param_manquant = type_franchise is None

    if param_manquant:
        message_param_manquant = u'Paramètre manquant sur la franchise manuelle.'
        ajouter_info(message_param_manquant)
        ajouter_avertissement(message_param_manquant)
        ajouter_erreur(message_param_manquant)
        return datetime.date(9999, 1, 1)
    else:
        if type_franchise == u'autre':
            dei_absente = datetime.date(9999,1,3)
        elif type_franchise == u'recccn':
            dei_absente = datetime.date(9999,1,4)
        elif type_franchise == u'relccn':
            dei_absente = datetime.date(9999,1,5)
        elif type_franchise == u'cumulee_annee_civile':
            dei_absente = datetime.date(9999,1,6)
        elif type_franchise == u'cumulee_annee_glissante':
            dei_absente = datetime.date(9999,1,7)

    # DONNEE
    date_debut_indemnisation = compl_date_effet_indemnisation()
    ajouter_info(date_debut_indemnisation)
    if date_debut_indemnisation is None:
        message_none = u"Aucune date d'effet d'indemnisation renseignée."
        ajouter_info(message_none)
        ajouter_avertissement(message_none)
        ajouter_erreur(message_none)
        message_debug(message_none)
        res = dei_absente # code dei manuelle non saisie
        return res
    elif not isinstance(date_debut_indemnisation, datetime.date):
        message_absence = u"Absence de date d'effet d'indemnisation."
        ajouter_info(message_absence)
        ajouter_avertissement(message_absence)
        ajouter_erreur(message_absence)
        message_debug(message_absence)
        res = dei_absente # code dei manuelle non date
        return res
    else:
        message_presence = u"Présence de date d'effet d'indemnisation."
        message_debug(message_presence)
        fin_franchise = ajouter_jours(date_debut_indemnisation, -1)
        return fin_franchise

return fr_saisie_manuelle() # DECOMMENTER SOUS COOG

##########################
# FIN FR SAISIE MANUELLE #
