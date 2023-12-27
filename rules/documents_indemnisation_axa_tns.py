# ---
# Name: Documents indemnisation AXA TNS
# Short Name: documents_indemnisation_axa_tns
# Type: doc_request
# ---

# DEBUT DOC INDEMN AXA TNS #
############################

def document_indemnisation_axa_tns():
    res = dict()

    statut_eligibilite = statut_eligibilite_prestation()
    if statut_eligibilite and statut_eligibilite != 'accepted':
        return res

    res['avis_d_arret_de_travail'] = {'blocking': True}
    res['justificatifs_IJ_secu'] = {'blocking': True}

    return res

return document_indemnisation_axa_tns() # DECOMMENTER SOUS COOG

##########################
# FIN DOC INDEMN AXA TNS #
