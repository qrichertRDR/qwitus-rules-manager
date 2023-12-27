# ---
# Name: Documents dossier inval
# Short Name: documents_dossier_inval
# Type: doc_request
# ---

# DEBUT DOC DOSSIER RI #
########################


def document_dossier_rente_inval():

       res = dict()

       statut_eligibilite = statut_eligibilite_prestation()
       if statut_eligibilite and statut_eligibilite != 'accepted':
              return res

       res.update({
              'declaration_d_invalidite_de_travail': {'blocking': True},
              'notification_de_pension_d_invalidite': {'blocking': True},
              'justificatif_pension_versee_ss': {'blocking': True},
              'rib_assure': {'blocking': True},
              'dernier_avis_imposition': {'blocking': True},
              'notification_de_prise_en_charge_pole_emploi': {'blocking': True},
              'justificatif_paiement_pole_emploi': {'blocking': True},
              'fiches_de_salaire': {'blocking': True},
              'fiche_de_salaire_a_compter_de_la_ri': {'blocking': True},
              'certificat_de_travail': {'blocking': True},
              'carte_d_identite': {'blocking': True},
              'accord_pec_medical': {'blocking': True}
       })

       return res

return document_dossier_rente_inval() # DECOMMENTER SOUS COOG


#####################
# FIN DOC DOSSER RI #
#####################
