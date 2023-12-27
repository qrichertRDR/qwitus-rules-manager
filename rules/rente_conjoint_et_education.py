# ---
# Name: Rente conjoint et education
# Short Name: rente_conjoint_et_education
# Type: benefit
# ---

# TODO fusionner avec sorties_iss
def sorties_rente_conjoint_education_corrigee_ou_nulle(precision=0.01):

    ############
    # CONTEXTE #
    ############
    dp = date_debut_periode_indemnisation()
    fp = date_fin_periode_indemnisation()
    nbj_p = (fp - dp).days + 1

    # STRUCTURE RESULTAT
    test_p = {
        "reference_j": 0,
        "contractuel_j": 0,
        "rente_j": 0,
        "prestation_j": 0,
        "prestation_rv_j": 0,
    }

    description = u""
    res_p = {
        'start_date': dp,
        'end_date': fp,
        'nb_of_unit': nbj_p,
        'unit': 'day',
        'amount': Decimal(0),
        'base_amount': Decimal(0),
        'amount_per_unit': Decimal(0),
        'description': description.encode("utf8"),
        #'extra_details': {
        #    'rass_brut': str(rass_b),
        #    'rass_net': str(rass_n),
        #},
        'test_data': test_p
    }

    res = [res_p]

    presta_base = compl_prestation_de_base_manuelle()
    revalo = compl_revalorisation_manuelle()
    description_calcul = compl_description_du_calcul()

    # SORTIE RENTE CONJOINT OU EDUCATION CORRIGEE
    if (presta_base is None) != (revalo is None):
        message_erreur = u"Un des montants de prestation n'est pas saisi."
        test_p['erreur'] = (-1, message_erreur)
        ajouter_erreur(message_erreur)
        return res

    if presta_base is not None and revalo is not None:

        if presta_base >= 0 and revalo >= 0:
            base_p = presta_base
            revalo_p = revalo

            if revalo_p >= base_p and not (base_p == revalo_p == 0):
                message_erreur = u'La revalorisation est supérieure à la base.'
                test_p['erreur'] = (-3, message_erreur)
                ajouter_avertissement(message_erreur)

            prestation_p = arrondir(presta_base + revalo, precision)

            if description_calcul is not None:
                description += description_calcul + u"\n"

            description += u"\nPRESTATION\n"
            description += u"Base (période) : %.2f€" % base_p
            description += u"\nRevalorisation (période) : %.2f€" % revalo_p
            description += u"\nPrestation (période) : %.2f€" % prestation_p

            res_p["amount"] = prestation_p
            res_p["base_amount"] = arrondir(base_p / nbj_p, precision)
            res_p["amount_per_unit"] = arrondir(prestation_p / nbj_p, precision)
            res_p["description"] = description.encode('utf8')

            test_p["prestation_j"] = res_p["base_amount"]
            test_p["prestation_rv_j"] = res_p["amount_per_unit"]
            message_debug(description)
            return res
        else:
            message_erreur = u"Un des montants de prestation corrigée est négatif."
            test_p['erreur'] = (-2, message_erreur)
            ajouter_erreur(message_erreur)
            return res

    return None


########################
# FIN PARTIE GENERIQUE #
########################


##########################################
# DEBUT RENTE CONJOINT EDUCATIONMANUELLE #
##########################################


def rente_conjoint_education_manuelle():

    # TODO gestion durée max ?
    # TODO gestion revalorisation prestation ?

    # DONNEES

    res_rente_conjoint_education_corrigee_ou_nulle = sorties_rente_conjoint_education_corrigee_ou_nulle()

    if res_rente_conjoint_education_corrigee_ou_nulle is not None:
        return res_rente_conjoint_education_corrigee_ou_nulle

    message_erreur = u"Merci de saisir une rente manuelle."
    ajouter_erreur(message_erreur)
    return

return rente_conjoint_education_manuelle() # RENTE CONJOINT EDUCATION # DECOMMENTER SOUS COOG

#########################################
# FIN RENTE CONJOINT EDUCATION MANUELLE #
#########################################
