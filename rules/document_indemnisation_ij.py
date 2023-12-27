# ---
# Name: Document indemnisation IJ
# Short Name: document_indemnisation_ij
# Type: doc_request
# ---

if service_deductible():
    return {}
res = {'justificatifs_IJ_secu': {'blocking': True}} if not avec_bpij() else {}
if nombre_jours_hospitalisation_prejudice() > 0:
    res['bulletin_de_situation'] = {'blocking': True}
if montant_de_deduction('part_time', date_debut_periode_indemnisation(), date_fin_periode_indemnisation(), False):
    res['justificatif_mi-temps_therapeutique'] = {'blocking': True}
return res
