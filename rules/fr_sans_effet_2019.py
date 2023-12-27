# ---
# Name: Franchise sans effet (nouveau)
# Short Name: fr_sans_effet_2019
# Type: benefit_deductible
# ---

# DEBUT FR SANS EFFET #
#######################
def fr_sans_effet():
    """
    :return: date de début d'indemnisation immédiate
    :rtype: datetime
    """
    ddp = date_de_debut_du_prejudice()
    if ddp is None:
        ajouter_erreur(u"Date de début du préjudice non renseignée.")
        return

    ff = ajouter_jours(ddp, -1)
    return ff

return fr_sans_effet() # DECOMMENTER SOUS COOG

#####################
# FIN FR SANS EFFET #
