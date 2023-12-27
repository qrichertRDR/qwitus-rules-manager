# ---
# Name: Demande de document dossier IJ
# Short Name: demande_de_document_dossier_ij
# Type: doc_request
# ---

res = {}
if service_deductible():
    return res
if nombre_jours_hospitalisation_prejudice() > 0:
    res['bulletin_de_situation'] = {'blocking': True}
if est_une_rechute():
    res['attestation_de_rechute'] = {'blocking': True}
res.update({
    'declaration_d_incapacite_de_travail': {'blocking': True},
    'fiches_de_salaire': {'blocking': True},
    'justificatifs_IJ_secu': {'blocking': True},
     })
return res
