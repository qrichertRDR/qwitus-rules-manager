# ---
# Name: Eligibilité Mensu CCN Labo
# Short Name: eligibilite_mensu_ccnlabo
# Type: benefit
# ---

# DEBUT EL IJ #
###############

def el_eligibilite_prestation_ij():

    description = 'EL ELIGIBILITE PRESTATION IJ\n'

    gestion_accident = compl_0a_gestion_accident()
    gestion_accident_travail = compl_0b_gestion_accident_du_travail()
    gestion_maladie = compl_0c_gestion_maladie()
    gestion_maladie_professionnelle = compl_0d_gestion_maladie_professionnelle()
    gestion_maternite = compl_0e_gestion_maternite()

    evenement = code_de_l_evenement_du_prejudice()

    liste_evt = ['accident',
                 'accident_du_travail',
                 'maladie',
                 'maladie_professionnelle',
                 'maternite']

    liste_gestion = [gestion_accident, gestion_accident_travail,
                         gestion_maladie, gestion_maladie_professionnelle,
                         gestion_maternite]

    liste_message = ["l'accident",
                     "l'accident du travail",
                     'la maladie',
                     'la maladie professionnelle',
                     'la maternité']

    dico_gestion = {
        liste_evt[0]: (liste_gestion[0], liste_message[0]),
        liste_evt[1]: (liste_gestion[1], liste_message[1]),
        liste_evt[2]: (liste_gestion[2], liste_message[2]),
        liste_evt[3]: (liste_gestion[3], liste_message[3]),
        liste_evt[4]: (liste_gestion[4], liste_message[4])
    }

    res = dico_gestion.get(evenement, 'Evènement invalide %s' % evenement)

    if isinstance(res, str):
        ajouter_erreur(res)
        return False

    gestion, message = res
    if gestion is None:
        message_none = 'Eligibilité non paramétrée pour le motif %s.' % evenement
        ajouter_info(message_none)
        return False
    elif not gestion:
        message = 'Pas de gestion de %s.' % message
        ajouter_info(message)
        return False

    message_debug(description)

    res, information, avertissement, erreur = rule_eligibilite_privee()

    dateanciennete = compl_dateanciennete()
    if (dateanciennete is None):
        information = "Pas de date d'ancienneté renseignée"
        ajouter_info(information)
        #ajouter_erreur("Pas de date d'ancienneté renseignée")
        res = False
    else:
        anciennete = jours_entre(dateanciennete, date_de_debut_du_prejudice())/365
        if anciennete<1:
            res = False
            information = "Ancienneté < 1 an"
            ajouter_info(information)

    if information != '':
        ajouter_info(information)
    if avertissement != '':
        ajouter_avertissement(avertissement)
    if erreur != '':
        ajouter_erreur(erreur)
    message_debug(res)
    return res

return el_eligibilite_prestation_ij() # DECOMMENTER SOUS COOG

#############
# FIN EL IJ #
