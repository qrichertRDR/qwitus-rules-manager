# ---
# Name: Document indemnisation Rente
# Short Name: document_indemnisation_rente
# Type: doc_request
# ---

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
date_passage_rente = date_de_debut_du_prejudice()
res = {}

justificatif_ss_requis = False
# On demande le justificatif SS à l'ouverture de la rente
if date_passage_rente == date_debut_periode:
    justificatif_ss_requis = True
# On demande le justificatif de la rente ss à la date anniversaire 
if not justificatif_ss_requis:
    date_anniversaire = ajouter_annees(date_passage_rente, 1)
    while date_anniversaire <= date_fin_periode:
        if date_anniversaire >= date_debut_periode:
            justificatif_ss_requis = True
            break
        date_anniversaire = ajouter_annees(date_anniversaire, 1)
if justificatif_ss_requis:
    res['justificatif_pension_versee_ss'] = {'blocking': True}

# on demande les justificatifs de prestations annexes si la période contient des prestations annexes
if montant_de_deduction('part_time', date_debut_periode, date_fin_periode, False):
    res['justificatif_mi-temps_therapeutique'] = {'blocking': True}
if montant_de_deduction('pole_emploi', date_debut_periode, date_fin_periode, False):
    res['justificatif_paiement_pole_emploi'] = {'blocking': True}
if montant_de_deduction('autres_revenus', date_debut_periode, date_fin_periode, False):
    res['justificatif_autres_revenus'] = {'blocking': True}

# on demande les justificatifs de prestations annexes si la période précédente contient des prestations annexes
if date_passage_rente < date_debut_periode:
    date_periode_precedente = ajouter_jours(date_debut_periode, -1)
    if montant_de_deduction('part_time', date_periode_precedente, date_periode_precedente, False):
        res['justificatif_mi-temps_therapeutique'] = {'blocking': True}
    if montant_de_deduction('pole_emploi', date_periode_precedente, date_periode_precedente, False):
        res['justificatif_paiement_pole_emploi'] = {'blocking': True}
    if montant_de_deduction('autres_revenus', date_periode_precedente, date_periode_precedente, False):
        res['justificatif_autres_revenus'] = {'blocking': True}
    
return res
