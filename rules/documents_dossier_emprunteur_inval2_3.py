# ---
# Name: Documents dossier emprunteur INVAL2/3
# Short Name: documents_dossier_emprunteur_inval2_3
# Type: doc_request
# ---

# DEBUT DOC DOSSIER EMP INVAL R2 R3 #
#####################################


def documents_dossier_emprunteur_inval2_3():
    res = dict()

    statut_eligibilite = statut_eligibilite_prestation()
    if statut_eligibilite and statut_eligibilite != 'accepted':
        return res

    res['tableau_amortissement_actualise_als'] = {'blocking': True}
    res['formulaire_declaration_at_assure'] = {'blocking': True}
    res['formulaire_info_sinistre_assure'] = {'blocking': True}
    res['accord_medecin_conseil'] = {'blocking': True}
    res['consentement_traitement_des_donnees'] = {'blocking': True}

    tns = compl_travailleur_non_salarie()
    if tns is None:
        ajouter_avertissement("Donnée Travailleur Non Salarié absente.")
        return res

    # Salariés
    if not tns:
        res['justificatifs_rentes_de_la_securite_sociale'] = {'blocking': True}
    # Travailleurs non salariés
    else:
        res['inscription_registre_du_commerce'] = {'blocking': True}
        res['avis_d_arret_de_travail'] = {'blocking': True}

    return res

return documents_dossier_emprunteur_inval2_3() # DECOMMENTER SOUS COOG


###################################
# FIN DOC DOSSIER EMP INVAL R2 R3 #
