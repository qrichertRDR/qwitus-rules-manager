# ---
# Name: Documents dossier AXA TNS IJ
# Short Name: documents_dossier_axa_tns_ij
# Type: doc_request
# ---

# DEBUT DOC DOSSIER AXA TNS IJ #
################################


def document_dossier_axa_tns_ij():
    res = dict()

    statut_eligibilite = statut_eligibilite_prestation()
    if statut_eligibilite and statut_eligibilite != 'accepted':
        return res

    if nombre_jours_hospitalisation_prejudice() > 0:
        res['bulletin_de_situation'] = {'blocking': True}

    if est_une_rechute():
        res['attestation_de_rechute'] = {'blocking': True}

    res.update({
        'declaration_d_incapacite_de_travail': {'blocking': True},
        'avis_d_arret_de_travail_initial': {'blocking': True},
        'carte_d_identite': {'blocking': True},
        'rib_assure': {'blocking': True}
    })

    return res

return document_dossier_axa_tns_ij() # DECOMMENTER SOUS COOG


##############################
# FIN DOC DOSSIER AXA TNS IJ #
