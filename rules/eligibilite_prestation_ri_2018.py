# ---
# Name: Eligibilité RI (nouveau)
# Short Name: eligibilite_prestation_ri_2018
# Type: benefit
# ---

# DEBUT EL RI #
###############

def el_eligibilite_prestation_ri():
    description = 'EL ELIGIBILITE PRESTATION RI\n'

    categorie = compl_categorie_de_rente_d_invalidite()

    gestion_r1 = compl_0a_gestion_r1()
    gestion_r2 = compl_0b_gestion_r2()
    gestion_r3 = compl_0c_gestion_r3()
    gestion_rat = compl_0d_gestion_rat()

    liste_categorie = ['r1',
                       'r2',
                       'r3',
                       'rat']
    liste_gestion = [gestion_r1, gestion_r2, gestion_r3, gestion_rat]

    dico_gestion = {
        liste_categorie[0]: (liste_gestion[0], liste_categorie[0]),
        liste_categorie[1]: (liste_gestion[1], liste_categorie[1]),
        liste_categorie[2]: (liste_gestion[2], liste_categorie[2]),
        liste_categorie[3]: (liste_gestion[3], liste_categorie[3])
    }

    res = dico_gestion.get(categorie, 'Catégorie de rente invalide %s' % categorie)

    if isinstance(res, str):
        ajouter_erreur(res)
        return False

    gestion, message = res
    if not gestion:
        message = 'Pas de gestion de %s.' % message
        ajouter_info(message)
        return False

    if categorie in ['r1',
                     'r2',
                     'r3',
                     'rat']:

        rass_brute = compl_rass_brut()
        if rass_brute is None:
            message = 'RSS %s brute non renseignée.' % categorie
            ajouter_info(message)
            return False

        rass_nette = compl_rass_net()
        if rass_nette is None:
            message = 'RSS %s nette non renseignée.' % categorie
            ajouter_info(message)
            return False

        if categorie == 'rat':
            tip = compl_taux_incapacite_permanente()
            if tip is None:
                message = "Taux d'incapacité permanente non renseigné."
                ajouter_info(message)
                return False

    message_debug(description)
    res, information, avertissement, erreur = rule_eligibilite_privee()
    if information != '':
        ajouter_info(information)
    if avertissement != '':
        ajouter_avertissement(avertissement)
    if erreur != '':
        ajouter_erreur(erreur)

    return res

return el_eligibilite_prestation_ri() # DECOMMENTER SOUS COOG

#############
# FIN EL RI #
