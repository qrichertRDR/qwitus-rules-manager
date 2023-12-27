# ---
# Name: Règle analyse médicale générale
# Short Name: regle_analyse_medicale_generale
# Type: underwriting_type
# ---

# DEBUT AM STANDARD #
#####################


'''
Nom : Règle analyse médicale générale
Code : regle_analyse_medicale_generale
Type : Type de demande de décisions
Type du résultat : 
Contexte : Context par défaut
Statut : Validé

Tables : Règles_Analyses_Médicales_Cie
'''


def initier_am():
    # Règle de déclenchement de l'analyse médicale

    # CAS ERREUR
    # absence de la compagnie KO
    # absence ou valeur invalide de l'analyse médicale (OUI, NON) OK
    # Si analyse médicale : absence ou valeur invalide de la décision, de la date d'effet OK

    # PAS D'ANALYSE MEDICALE EN CAS DE MATERNITE
    if code_de_l_evenement_du_prejudice() == 'maternite':
        return None, None

    decision_par_defaut = 'analyse_medicale_bloquante'
    date_par_defaut = date_fin_franchise()

    code_assureur = champs_technique(
        'service.option.coverage.insurer.party.code')
    cie = code_assureur[2:]
    message_debug(u'\nCompagnie %s' % cie)

    attribut_analyse_medicale = 'ANALYSE_MED'
    valeur_analyse_medicale = table_regles_analyses_medicales_cie(
        cie, attribut_analyse_medicale)
    message_debug(u'\nAnalyse médicale %s' % valeur_analyse_medicale)

    if valeur_analyse_medicale == 'NON':
        return None, None
    elif valeur_analyse_medicale == 'OUI':
        attribut_reference = 'REFERENCE'
        valeur_reference = table_regles_analyses_medicales_cie(
            cie, attribut_reference)
        message_debug(u'\nRéférence %s' % valeur_reference)

        # DATE APPLICATION
        date = None
        if valeur_reference == u'DAT':
            date = date_debut_arret_de_travail()
        elif valeur_reference == u'DEI':
            date = ajouter_jours(date_fin_franchise(), 1)
        else:
            message = u'\nDate de départ incorrecte %s.' % valeur_reference
            ajouter_erreur(message)
            return decision_par_defaut, date_par_defaut

        attribut_nbj = 'NBJ'
        valeur_nbj = Decimal(table_regles_analyses_medicales_cie(
            cie, attribut_nbj))
        message_debug(u'\nNbj %s' % valeur_nbj)

        date = ajouter_jours(date, valeur_nbj)

        # DECISION
        attribut_decision = 'DECISION'
        valeur_decision = table_regles_analyses_medicales_cie(
            cie, attribut_decision)
        message_debug(u'\nDécision %s' % valeur_decision)

        # AVANT ATTM
        attribut_avant_attm = 'AVANT_ATTM'
        valeur_avant_attm = table_regles_analyses_medicales_cie(
            cie, attribut_avant_attm)
        message_debug(u'\nAvant attestation médicale %s' % valeur_avant_attm)

        decision = None
        if valeur_avant_attm == 'ACCEPTE':
            if valeur_decision == 'ACCEPTE':
                decision = 'analyse_medicale_non_bloquante'
            elif valeur_decision == 'BLOCAGE':
                decision = 'analyse_medicale_non_bloquante_puis_bloquante'
            else:
                message_erreur = u'Décision non prévue : %s.' % valeur_decision
                ajouter_erreur(message_erreur)
                return decision_par_defaut, date_par_defaut
        elif valeur_avant_attm == 'BLOCAGE':
            if valeur_decision == 'BLOCAGE':
                decision = 'analyse_medicale_bloquante'
            elif valeur_decision == 'ACCEPTE':
                decision = 'analyse_medicale_bloquante_puis_non_bloquante'
            else:
                message_erreur = u'Décision non prévue : %s.' % valeur_decision
                ajouter_erreur(message_erreur)
                return decision_par_defaut, date_par_defaut
        else:
            message_erreur = \
                u'Décision avant attestation médicale non prévue: %s.' \
                % valeur_avant_attm
            ajouter_erreur(message_erreur)
            return decision_par_defaut, date_par_defaut

        return decision, date
    else:
        message_erreur = \
             u'Analyse médicale invalide %s' % valeur_analyse_medicale
        ajouter_erreur(message_erreur)
        return decision_par_defaut, date_par_defaut

return initier_am() # DECOMMENTER SOUS COOG

###################
# FIN AM STANDARD #
