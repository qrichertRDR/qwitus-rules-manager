# ---
# Name: Changement compagnie (gestion contrat)
# Short Name: cgt_gestion_contrat
# Type: tool
# ---

# DEBUT CGT GESTION COTNRAT #
###################################

def rule_cgt_gestion_contrat():

    deb = date_debut_periode_indemnisation()
    fin = date_fin_periode_indemnisation()
    dev = date_de_debut_du_prejudice()

    # AFFILIATION
    '''
    c_per_aff_np = 'service.covered_element.num_period'
    c_per_aff_deb = 'service.covered_element.manual_start_date'
    c_per_aff_fin = 'service.covered_element.manual_end_date'

    per_aff_np = champs_technique(c_per_aff_np)
    per_aff_deb = champs_technique(c_per_aff_deb)
    per_aff_fin = champs_technique(c_per_aff_fin)

    message_debug(u'%s %s %s' % (per_aff_np, formater_date(per_aff_deb), formater_date(per_aff_fin)))
    '''

    base_ass_n = montant_base_ancien_assureur()
    reva_ass_n = revalorisation_ancien_assureur()

    regle_entree = None
    date_entree = None

    # CONTEXTE ASSUREUR 2+ (ON S'INTERESSE AUX DATES ET REGLES D'ENTREE OBLIGATOIRE (ET DE SORTIE EVENTUELLE))
    if base_ass_n is not None and reva_ass_n is not None:

        # PERIODE
        prefix_ass2 = 'custom_roederer_service.'
        c_per_ent_np = prefix_ass2 + 'covered_element.parent.num_period'

        # ENTREE
        c_per_ent_deb = prefix_ass2 + 'covered_element.parent.manual_start_date'
        c_regle_sortie_ass1 = 'contract.post_termination_claim_behaviour'
        regle_sortie_ass1 = champs_technique(c_regle_sortie_ass1)
        regle_entree = regle_sortie_ass1

        if regle_entree == 'normal_indemnifications':
            message_debug(u'REPRISE : LIMITER A 0€')
        elif regle_entree == 'stop_indemnifications':
            message_debug(u'REPRISE : NE PAS LIMITER')
        elif regle_entree == 'lock_indemnifications':
            message_debug(u'REPRISE : LIMITER AU DELA DU NIVEAU ATTEINT AU %s' % date_entree)

        # SORTIE EVENTUELLE
        c_statut_contrat = prefix_ass2 + 'covered_element.parent.contract.status'
        c_regle_sortie = prefix_ass2 + 'covered_element.parent.contract.post_termination_claim_behaviour'
        c_per_ent_fin = prefix_ass2 + 'covered_element.parent.manual_end_date'

    # CONTEXTE ASSUREUR 1 (ON S'INTERESSE AUX DATES ET REGLES DE SORTIE EVENTUELLE)
    else:

        # PERIODE
        c_per_ent_np = 'service.covered_element.parent.num_period'

        # ENTREE
        c_per_ent_deb = 'service.covered_element.parent.manual_start_date'

        # SORTIE EVENTUELLE
        c_statut_contrat = 'contract.status'
        c_regle_sortie = 'contract.post_termination_claim_behaviour'
        c_per_ent_fin = 'service.covered_element.parent.manual_end_date'

        '''
        c_regle_reprise = 'option.previous_claims_management_rule'
        regle_reprise = champs_technique(c_regle_reprise)
        message_debug(regle_reprise)
        '''

    # PERIODE
    per_ent_np = champs_technique(c_per_ent_np)
    message_debug(per_ent_np)

    # ENTREE
    per_ent_deb = champs_technique(c_per_ent_deb)
    date_entree = per_ent_deb

    # SORTIE
    statut_contrat = champs_technique(c_statut_contrat)
    per_ent_fin = champs_technique(c_per_ent_fin)
    regle_sortie = champs_technique(c_regle_sortie)
    date_sortie = per_ent_fin

    exception = (base_ass_n is not None \
                and reva_ass_n is not None \
                and date_entree is not None \
                and date_entree <= dev) \
                or \
                (base_ass_n is None
                 and reva_ass_n is None
                 and date_sortie is not None
                 and date_sortie < dev)

    # CONTRAT TERMINE
    if statut_contrat == 'terminated':

        # REGLE DE SORTIE ABSENTE
        if regle_sortie is None:
            message_erreur = 'Regle de sortie de gestion du contrat indéfinie.'
            ajouter_erreur(message_erreur)
            return None

        if date_sortie is None:
            message_erreur = 'Date de fin de revalorisation indéfinie.'
            ajouter_erreur(message_erreur)
            return None

        # TEST DEB PERIODE <= CGT CIE < FIN PERIODE : ERREUR RESAISIR EN SEPARANT CORRECTEMENT
        if deb <= date_sortie and fin > date_sortie:
            message_erreur = u"Cette période traverse un changement d'assureur " \
                             u"au %s, " \
                             u"merci de saisir deux périodes." % date_sortie
            ajouter_erreur(message_erreur)
            return None

        # PERIODE INDEMNISATION > FIN DE PERIODE ENTREPRISE
        if deb > date_sortie:
            message_debug('PERIODE APRES SORTIE')
            if regle_sortie == 'normal_indemnifications':
                message_debug(u'SORTIE : NE PAS LIMITER')
            elif regle_sortie == 'stop_indemnifications':
                message_debug(u'SORTIE : LIMITER A 0€')
            elif regle_sortie == 'lock_indemnifications':
                message_debug(
                    u'SORTIE : LIMITER AU NIVEAU ATTEINT AU %s' % date_sortie)

    return regle_entree, regle_sortie, date_entree, date_sortie, exception

return rule_cgt_gestion_contrat() # DECOMMENTER SOUS COOG

###########################
# FIN CGT GESTION COTNRAT #
