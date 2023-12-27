# ---
# Name: Règle de contrôle des prestations
# Short Name: regle_de_controle_des_prestations
# Type: benefit
# ---

# DEBUT REGLE CONTROLE PRESTATION #
###################################


def regle_de_controle_des_prestation():
    if code_du_descriteur_du_prejudice() in ['arret_de_travail', 'invalidite',
                                             'DC']:
        dp = date_debut_periode_indemnisation()
        fp = date_fin_periode_indemnisation()
        if fp is None:
            fp = dp
        salaire = salaire_net() or salaire_brut()
        if salaire >= 100000:
            return True, u'Salaire de référence supérieur à 100 000€ : %s€'\
                   % salaire
        if maximum_prestations_journalieres() > 100:
            return True, u'Indémnités journalières supérieure à 100€'
        if entier_aleatoire(0, 99) < 5:
            return True, u'Contrôle aléatoire'
        if jours_entre(dp, fp) > 180:
            return True, u'Indémnisation supérieure à 6 mois'
        if compl_ij_de_base_corrige():
            return True, u'Indémnisation journalière manuellement définie'
        if compl_ri_corrigee():
            return True, u'Rente journalière manuellement définie'
        if compl_prestation_de_base_manuelle():
            return True, u'Rente conjoint manuellement définie'

    if code_du_descriteur_du_prejudice() in ['invalidite', 'DC']:
        return True, u'Rente contrôle systématique'

    return False, ''


return regle_de_controle_des_prestation() # DECOMMENTER SOUS COOG

#################################
# FIN REGLE CONTROLE PRESTATION #
