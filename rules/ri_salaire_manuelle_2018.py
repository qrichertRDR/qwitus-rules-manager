# ---
# Name: Rente manuelle (nouveau)
# Short Name: ri_salaire_manuelle_2018
# Type: benefit
# ---

# DEBUT RI MANUELLE #
#####################


def donnees_rente():  # RI MANUELLE
    '''
    :données complémentaires:
        - rjss
        - ri_corrigee
        - description_ri_de_base_corrige
    :return:
    :rtype: list[dict[str,any]]
    '''

    ###########
    # DONNEES #
    ###########

    # EVENEMENT
    cat = compl_categorie_de_rente_d_invalidite()
    rass_b = compl_rass_brut()
    rass_n = compl_rass_net()
    tip = compl_taux_incapacite_permanente()

    # TESTS
    if cat is None:
        message_none = 'Catégorie de rente non saisie.'
        ajouter_erreur(message_none)
        return

    if rass_b is None:
        message_none = 'RSS brute non saisie.'
        ajouter_erreur(message_none)
        return

    if rass_n is None:
        message_none = 'RSS nette non saisie.'
        ajouter_erreur(message_none)
        return

    rass1_b, rass1_n = None, None
    rass2_b, rass2_n = None, None
    rass3_b, rass3_n = None, None
    rassat_b, rassat_n = None, None

    cinq = Decimal(5)
    trois = Decimal(3)

    if cat == 'r1':
        coef = cinq / trois
        rass1_b, rass1_n = rass_b, rass_n
        rass2_b, rass2_n = rass_b * coef, rass_n * coef
        rass3_b, rass3_n = rass2_b, rass2_n
    elif cat == 'r2':
        rass2_b, rass2_n = rass_b, rass_n
    elif cat == 'r3':
        rass3_b, rass3_n = rass_b, rass_n
    elif cat == 'rat':
        rassat_b, rassat_n = rass_b, rass_n

    categories = {
        'r1': (rass1_b, rass1_n, '1'),
        'r2': (rass2_b, rass2_n, '2'),
        'r3': (rass3_b, rass3_n, '3'),
        'rat': (rassat_b, rassat_n, 'AT'),
    }

    res = categories.get(cat, 'Catégorie de rente invalide %s' % cat)
    if isinstance(res, str):
        ajouter_erreur(res)
        return

    rass_b, rass_n, label = res
    res = rass_b is None and rass_n is None
    if res:
        message = 'RSS de catégorie %s non renseignées.' % label
        ajouter_erreur(message)
        return

    if cat == 'rat':
        if tip is None:
            message = "Taux d'incapacité permanente non renseigné."
            ajouter_erreur(message)
            return

    return cat, \
           rass1_b, rass1_n, \
           rass2_b, rass2_n, \
           rass3_b, rass3_n, \
           rassat_b, rassat_n, tip, \
           rass_b, rass_n


###################
# FIN RI MANUELLE #
# DEBUT RI MANUELLE #
#####################

def sorties_rss_corrigee_ou_nulle(rass_b, rass_n, precision=0.01):

    ############
    # CONTEXTE #
    ############
    dp = date_debut_periode_indemnisation()
    fp = date_fin_periode_indemnisation()
    nbj_p = (fp - dp).days + 1

    # STRUCTURE RESULTAT
    test_p = {
        'reference_j': 0,
        'contractuel_j': 0,
        'rente_j': 0,
        'prestation_j': 0,
        'prestation_rv_j': 0,
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
            'rass_brut': str(rass_b),
            'rass_net': str(rass_n),
        },
        'test_data': test_p
    }

    res = [res_p]

    ri_base_corrigee_p = compl_ri_corrigee()
    ri_revalo_corrigee_p = compl_ri_revalo_corrigee()
    desc_ri_corrigee_p = compl_description_ri_de_base_corrige()

    # SORTIE RI CORRIGEE
    if (ri_base_corrigee_p is None) != (ri_revalo_corrigee_p is None):
        message_erreur = "Un montant de prestation corrigée n'est pas saisi."
        test_p['erreur'] = (-1, message_erreur)
        ajouter_erreur(message_erreur)
        return res

    if ri_base_corrigee_p is not None and ri_revalo_corrigee_p is not None:

        if ri_base_corrigee_p >= 0 and ri_revalo_corrigee_p >= 0:
            base_p = ri_base_corrigee_p
            revalo_p = ri_revalo_corrigee_p

            if revalo_p >= base_p and not (base_p == revalo_p == 0):
                message_erreur = 'La revalorisation corrigée est supérieure' \
                                 ' à la base corrigée.'
                test_p['erreur'] = (-3, message_erreur)
                ajouter_avertissement(message_erreur)

            presta_p = arrondir(
                ri_base_corrigee_p + ri_revalo_corrigee_p, precision
            )

            if desc_ri_corrigee_p is not None:
                description += desc_ri_corrigee_p + '\n'

            description += '\nPRESTATION\n'
            description += 'Base (période) : %.2f€' % base_p
            description += '\nRevalorisation (période) : %.2f€' % revalo_p
            description += '\nPrestation (période) : %.2f€' % presta_p

            res_p['amount'] = presta_p
            res_p['base_amount'] = arrondir(base_p / Decimal(nbj_p), precision)
            res_p['amount_per_unit'] = arrondir(presta_p / Decimal(nbj_p), precision)
            res_p['description'] = description

            test_p['prestation_j'] = \
                res_p['base_amount']
            test_p['prestation_rv_j'] = \
                res_p['amount_per_unit']
            message_debug(description)
            return res
        else:
            message_erreur = 'Un montant de prestation corrigée est négatif.'
            test_p['erreur'] = (-2, message_erreur)
            ajouter_erreur(message_erreur)
            return res

    # SORTIE RJSS NULLE
    if rass_b is not None and rass_b <= 0 \
            and rass_n is not None and rass_n <= 0:
        description = 'Aucune prestation à verser car la RSS est nulle.\n'
        res_p['description'] = description
        message_debug(description)
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

###################
# FIN RI MANUELLE #
# DEBUT RI MANUELLE #
#####################


def ri_manuelle():

    # TODO gestion durée max ?
    # TODO gestion revalorisation prestation ?

    # DONNEES
    res = donnees_rente()
    if res is None:
        return

    cat, \
    rass1_b, rass1_n, \
    rass2_b, rass2_n, \
    rass3_b, rass3_n, \
    rassat_b, rassat_n, tip, \
    rass_b, rass_n = res

    res_rss_corrigee_ou_nulle = sorties_rss_corrigee_ou_nulle(rass_b, rass_n)

    if res_rss_corrigee_ou_nulle is not None:
        return res_rss_corrigee_ou_nulle

    message_erreur = 'Merci de saisir une rente corrigée.'
    ajouter_erreur(message_erreur)
    return

return ri_manuelle() # RI MANUELLE # DECOMMENTER SOUS COOG

###################
# FIN RI MANUELLE #
