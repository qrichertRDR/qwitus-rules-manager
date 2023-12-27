# ---
# Name: Indemnité Journalière manuelle (nouveau)
# Short Name: ij_salaire_manuelle_2018
# Type: benefit
# ---

# DEBUT IJ MANUELLE #
#####################


def recuperer_erreur(res):
    def dict_erreur(err):
        return type(err) is dict and \
                (err.get('erreur') or err.get('test_data', {}).get('erreur'))

    def tuple_erreur(err):
        return type(err) is tuple and len(err) == 2 and \
                type(err[0]) is int and err[0] < 0 and type(err[1]) is str

    if dict_erreur(res):
        return recuperer_erreur(res.get('erreur')) or res.get('erreur') or \
            recuperer_erreur(res.get('test_data', {}).get('erreur')) or \
            recuperer_erreur(res.get('test_data', {}))
    elif tuple_erreur(res):
        return res[1]
    elif type(res) is list:
        for elem in res:
            message_erreur = recuperer_erreur(elem)
            if message_erreur:
                return message_erreur


###################
# FIN IJ STANDARD #
###################

def si_erreur_lever_erreur(res):
    message = recuperer_erreur(res)
    if message:
        ajouter_erreur(message)
        return True
    return False


def si_avertissement_lever_avertissement(res):
    if type(res) is list and len(res) > 0 and res[0].get('avertissements'):
        for avertissement in res[0].pop('avertissements'):
            ajouter_avertissement(avertissement)
        return True
    return False

#####################
# DEBUT IJ STANDARD #
#####################

###################
# FIN IJ MANUELLE #
# DEBUT IJ MANUELLE #
#####################

def ij_manuelle():

    # TODO gestion durée max ?
    # TODO gestion revalorisation prestation ?

    # GENERAL

    # SORTIES PRIORITAIRES
    res_ijss_corrigee_ou_nulle = \
        rule_sorties_ijss_corrigee_ou_nulle(precision=None)
    si_erreur_lever_erreur(res_ijss_corrigee_ou_nulle)
    if res_ijss_corrigee_ou_nulle is not None:
        return res_ijss_corrigee_ou_nulle

    message_erreur = 'Merci de saisir une indemnité corrigée.'
    ajouter_erreur(message_erreur)
    return

return ij_manuelle() # DECOMMENTER SOUS COOG

###################
# FIN IJ MANUELLE #
