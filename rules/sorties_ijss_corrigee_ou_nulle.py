# ---
# Name: IJSS corrigée ou nulle
# Short Name: sorties_ijss_corrigee_ou_nulle
# Type: tool
# ---

# DEBUT IJSS CORRIGEE OU NULLE #
################################

def description_prestation_totale(prestation_j,
                                  nb_jours_prestation,
                                  prestation_t,
                                  type='ij',
                                  prestation_a=None):

    desc = '\nLa prestation réglée est de '
    if prestation_t == 0:
        desc += '%.2f€' % prestation_t
    elif prestation_t > 0:
        desc += '%.2f€ (%.2f€ × %s)' % (
        prestation_t, prestation_j, nb_jours_prestation)
    else:
        desc += '%.2f€ soit %.2f€' % (prestation_t, 0)
    return desc


def prestation_totale(prestation_j, dsp, fsp, precision=0.01): # IJ MANUELLE
    nb_jours_prestation = (fsp - dsp).days + 1
    prestation_t = prestation_j * nb_jours_prestation
    prestation_t = arrondir(prestation_t, precision)

    prestation_t = max(0, prestation_t)
    description = description_prestation_totale(prestation_j,
                                                nb_jours_prestation,
                                                prestation_t)
    return prestation_t, nb_jours_prestation, description

##############################
# FIN IJSS CORRIGEE OU NULLE #
# DEBUT IJSS CORRIGEE OU NULLE #
################################

def sorties_ijss_corrigee_ou_nulle():
    '''
    .. todo :: Externaliser dans un autre fichier
    '''
    precision = param_precision()
    if precision is None:
        precision = 0.01
    return rule_sorties_ijss_corrigee_ou_nulle(precision=precision)

# TODO fusionner avec sorties_rjss
def rule_sorties_ijss_corrigee_ou_nulle(precision): # IJ MANUELLE

    ###########
    # CONTEXTE #
    ############
    dp = date_debut_periode_indemnisation()
    fp = date_fin_periode_indemnisation()
    nbj_p = (fp - dp).days + 1

    iss_j, iss_sanction_j, ib_base_corrigee_j, ib_revalo_corrigee_j, \
    desc_ib_corrigee_j, _ = donnees_generiques()

    # STRUCTURE RESULTAT
    test_p = {
        'reference_j': Decimal(0),
        'contractuel_j': Decimal(0),
        'indemnite_base_j': Decimal(0),
        'prestation_j': Decimal(0),
        'prestation_rv_j': Decimal(0)
    }

    description = ''
    res_p = {
        'start_date': dp,
        'end_date': fp,
        'nb_of_unit': nbj_p,
        'unit':
            'day',
        'amount': Decimal(0),
        'base_amount': Decimal(0),
        'amount_per_unit': Decimal(0),
        'description': description,
        'extra_details': {
            # TODO taux conversion
            'ijss': str(iss_j),
            'sanction_ijss': str(iss_sanction_j),
        },
        'test_data': test_p
    }

    res = [res_p]

    # SORTIE IJ CORRIGEE
    if (ib_base_corrigee_j is None) != (ib_revalo_corrigee_j is None):
        message_erreur = "Un des montants de prestation corrigée n'est pas saisi."
        test_p['erreur'] = (-1, message_erreur)
        return res

    if ib_base_corrigee_j is not None and ib_revalo_corrigee_j is not None:
        if ib_base_corrigee_j >= 0 and ib_revalo_corrigee_j >= 0:
            base_j = ib_base_corrigee_j
            revalo_j = ib_revalo_corrigee_j

            if revalo_j >= base_j and not (base_j == revalo_j == 0):
                message_erreur = 'La revalorisation corrigée est supérieure à la base corrigée.'
                test_p['erreur'] = (-3, message_erreur)
                return res

            prestation_j = arrondir(ib_base_corrigee_j + ib_revalo_corrigee_j, precision)

            if desc_ib_corrigee_j is not None:
                description += desc_ib_corrigee_j + '\n'

            description += '\nPRESTATION\n'
            description += 'Base (journalière) : %.2f€' % base_j
            description += '\nRevalorisation (journalière) : %.2f€' % revalo_j
            description += '\nPrestation (journalière) : %.2f€' % prestation_j

            prestation_t, _, desc = prestation_totale(prestation_j, dp, fp)
            description += desc

            res_p['amount'] = prestation_t
            res_p['base_amount'] = base_j
            res_p['amount_per_unit'] = prestation_j
            res_p['description'] = description

            test_p['prestation_j'] = \
                res_p['base_amount']
            test_p['prestation_rv_j'] = \
                res_p['amount_per_unit']
            message_debug(description)
            return res
        else:
            message_erreur = 'Un des montants de prestation corrigée est négatif.'
            test_p['erreur'] = (-2, message_erreur)
            return res


    # SORTIE IJSS NULLE
    if iss_j is not None and iss_j <= 0:
        description = "Aucune prestation à verser car l'IJSS est nulle\n"
        res_p['description'] = description
        message_debug(description)
        return res

    # SORTIE IJSS NONE
    if iss_j is None:
        message_erreur = 'Aucune IJSS saisie.'
        test_p['erreur'] = (-4, message_erreur)
        return res

    # SORTIE AUCUNE REPRISE / MAINTIEN
    res_sortie_contrat = rule_cgt_gestion_contrat()
    if res_sortie_contrat is None:
        return

    regle_entree, regle_sortie, date_entree, date_sortie, exception = res_sortie_contrat
    if (regle_entree and regle_entree == 'normal_indemnifications'):
        message_erreur = 'Aucune reprise.'
        test_p['erreur'] = (-5, message_erreur)
        description = 'Aucune prestation à verser car aucune reprise de prestation à partir du %s.' % formater_date(date_entree)
        res_p['description'] = description
        return res

    if (regle_sortie and date_sortie and regle_sortie == 'stop_indemnifications' and dp > date_sortie):
        message_erreur = 'Aucun maintien.'
        test_p['erreur'] = (-6, message_erreur)
        description = 'Aucune prestation à verser car aucun maintien de prestation après le %s.' % formater_date(date_sortie)
        res_p['description'] = description
        return res

    return None

##############################
# FIN IJSS CORRIGEE OU NULLE #
# DEBUT IJSS CORRIGEE OU NULLE #
################################

def donnees_generiques(): # IJ MANUELLE
    '''
    :données complémentaires:
        - ijss
        - sanction_ijss
        - ib_corrigee
    :return:
    :rtype: list[dict[str,any]]
    '''

    ijss = compl_ijss()
    taux_conversion_ijss = compl_taux_conversion_ijss_brut_vers_net()
    iss_sanction_j = compl_sanction_ijss()

    ib_base_corrigee_j = compl_ij_de_base_corrige()
    ib_revalo_corrigee_j = compl_ij_revalo_corrige()
    desc_ib_corrigee_j = compl_description_ij_de_base_corrige()

    return ijss, iss_sanction_j, ib_base_corrigee_j, ib_revalo_corrigee_j, \
           desc_ib_corrigee_j, taux_conversion_ijss

return sorties_ijss_corrigee_ou_nulle() # DECOMMENTER SOUS COOG

##############################
# FIN IJSS CORRIGEE OU NULLE #
