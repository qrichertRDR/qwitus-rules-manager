# ---
# Name: Documents dossier emprunteur Déces
# Short Name: documents_dossier_emprunteur_deces
# Type: doc_request
# ---

# DEBUT DOC DOSSIER EMP DECES #
###############################


def documents_dossier_emprunteur_deces():
    res = dict()

    statut_eligibilite = statut_eligibilite_prestation()
    if statut_eligibilite and statut_eligibilite != 'accepted':
        return res

    res['tableau_amortissement_actualise_als'] = {'blocking': True}
    res['formulaire_declaration_de_deces'] = {'blocking': True}
    res['acte_de_deces'] = {'blocking': True}
    res['justificatif_d_assurance'] = {'blocking': True}

    return res

return documents_dossier_emprunteur_deces() # DECOMMENTER SOUS COOG

#############################
# FIN DOC DOSSIER EMP DECES #
