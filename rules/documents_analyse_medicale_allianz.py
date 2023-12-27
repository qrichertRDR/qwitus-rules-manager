# ---
# Name: Documents analyse médicale Allianz
# Short Name: documents_analyse_medicale_allianz
# Type: doc_request
# ---

base = {
    'attestation_medicale': {'blocking': False},
    }
if code_de_l_evenement_du_prejudice() == 'accident':
    base['circonstances_de_l_accident'] = {'blocking': False}
return base
