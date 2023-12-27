# ---
# Name: Documents indemnisation emprunteur ITT INVAL1 
# Short Name: documents_indemnisation_emprunteur_itt_inval1
# Type: doc_request
# ---

# DEBUT DOC INDEMN EMP ITT INVAL1 #
###################################

def documents_indemnisation_emprunteur_itt_inval1():
    res = {}

    statut_eligibilite = statut_eligibilite_prestation()
    if statut_eligibilite and statut_eligibilite != 'accepted':
        return res

    tns = compl_travailleur_non_salarie()
    if tns is None:
        ajouter_avertissement("Donnée Travailleur Non Salarié absente.")
        return res

    # Salariés
    if not tns:
        # INVAL
        if code_du_descriteur_du_prejudice() == 'invalidite':
            res['justificatifs_rentes_de_la_securite_sociale'] = {
                'blocking': True
            }
        # ITT
        else:
            res['justificatifs_IJ_secu'] = {'blocking': True}

    # Travailleurs non salariés
    else:
        res['avis_d_arret_de_travail'] = {'blocking': True}

    return res

return documents_indemnisation_emprunteur_itt_inval1() # DECOMMENTER SOUS COOG

#################################
# FIN DOC INDEMN EMP ITT INVAL1 #
#################################
