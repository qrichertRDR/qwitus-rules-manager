# ---
# Name: Documents analyse médicale générale
# Short Name: documents_analyse_medicale_generale
# Type: doc_request
# ---

# DEBUT AM DOCUMENTS #
######################


'''
Nom : Documents analyse médicale générale
Code : documents_analyse_medicale_generale
Type : Demande de Documents
Type du résultat : Dictionnaire
Contexte : Context par défaut
Statut : Validé

Tables : Règles_Analyses_Médicales_Cie
'''


def apres_reception_am():
    # Règle de comportement à adopter avant réception de l'attestation médicale

    code_assureur = champs_technique(
        'service.option.coverage.insurer.party.code')
    cie = code_assureur[2:]
    message_debug(u'\nCompagnie %s' % cie)

    attribut_avant_attm = 'AVANT_ATTM'
    valeur_avant_attm = table_regles_analyses_medicales_cie(
        cie, attribut_avant_attm)
    message_debug(u'\nAvant attestation médicale %s' % valeur_avant_attm)

    base = {}
    if code_de_l_evenement_du_prejudice() == 'accident':
        base['circonstances_de_l_accident'] = {'blocking': False}

    if valeur_avant_attm == 'ACCEPTE':
        base['attestation_medicale'] = {'blocking': False}
    elif valeur_avant_attm == 'BLOCAGE':
        message_debug('blocage')
        base['attestation_medicale'] = {'blocking': True}
    else:
        # par défaut on met l'attestation médicale à bloquant
        message_erreur = \
            u'Avant attestation médicale invalide %s.' % valeur_avant_attm
        ajouter_erreur(message_erreur)
        base['attestation_medicale'] = {'blocking': True}

    return base

return apres_reception_am() # DECOMMENTER SOUS COOG

####################
# FIN AM DOCUMENTS #
