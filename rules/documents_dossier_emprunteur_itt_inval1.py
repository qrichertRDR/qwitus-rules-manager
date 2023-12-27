# ---
# Name: Documents dossier emprunteur ITT INVAL1 
# Short Name: documents_dossier_emprunteur_itt_inval1
# Type: doc_request
# ---

# DEBUT DOC DOSSIER EMP ITT INVAL #
###################################


def document_dossier_emprunteur_itt_inval1():
    res = dict()

    statut_eligibilite = statut_eligibilite_prestation()
    if statut_eligibilite and statut_eligibilite != 'accepted':
        return res

    tns = compl_travailleur_non_salarie()
    if tns is None:
        ajouter_avertissement("Donnée Travailleur Non Salarié absente.")
        return res

    res['tableau_amortissement_actualise_als'] = {'blocking': True}
    res['formulaire_declaration_at_assure'] = {'blocking': True}
    res['formulaire_info_sinistre_assure'] = {'blocking': True}
    res['rib_assure'] = {'blocking': True}
    res['attestation_medicale'] = {'blocking': True}
    res['consentement_traitement_des_donnees'] = {'blocking': True}

    if code_du_descriteur_du_prejudice() == 'invalidite':
        res['accord_medecin_conseil'] = {'blocking': True}

    if tns:
        res['inscription_registre_du_commerce'] = {'blocking': True}
        res['avis_d_arret_de_travail_initial'] = {'blocking': True}

    return res

return document_dossier_emprunteur_itt_inval1() # DECOMMENTER SOUS COOG

#################################
# FIN DOC DOSSIER EMP ITT INVAL #
