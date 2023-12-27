# ---
# Name: Demande de document dossier IJ AXA TNS
# Short Name: demande_de_document_dossier_ij_axa_tns
# Type: doc_request
# ---

res = {}
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
