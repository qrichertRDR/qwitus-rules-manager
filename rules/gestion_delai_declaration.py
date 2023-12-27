# ---
# Name: Gestion du délai de déclaration (nouveau, prive)
# Short Name: gestion_delai_declaration
# Type: tool
# ---

# DEBUT GESTION DELAI DECLARATION #
###################################

def rule_gestion_delai_declaration(date_fin_franchise_initiale):
    res, date_decla, date_decla_max, information, avertissement, erreur, desc_delai_decla = \
        True, \
        datetime.date(9999,1,1), \
        datetime.date(1,1,1), \
        '', \
        '', \
        '', \
        ''
    delta_decla = (date_decla - date_decla_max).days + 1

    # RECUPERATION FRANCHISE MANUELLE
    fin_franchise = date_fin_franchise_initiale
    if fin_franchise is None:
        res = False
        message = "Date d'effet d'indemnisation introuvable."
        information, avertissement, erreur = message, message, message
        ajouter_info(message)
        ajouter_avertissement(message)
        return res, date_decla, date_decla_max, delta_decla, information, avertissement, erreur, desc_delai_decla

    desc_delai_decla += '\tFin franchise : %s\n' % formater_date(fin_franchise)

    # RECUPERATION DU TYPE DE DELAI DE DECLARATION (SANS LIMITE, FIXE, VARIABLE SELON LA FRANCHISE)
    debut_arret_travail = date_de_debut_du_prejudice()

    utilisation_pivot = compl_2a_delai_declaration_variable()
    declaration_quantite = 0
    declaration_definition = ''

    if utilisation_pivot == 'sans_limite':
        declaration_definition = 'sans_limite'
    elif utilisation_pivot == 'fixe':
        declaration_quantite = compl_2b_delai_declaration()
        declaration_definition = compl_2c_delai_declaration_definition()
    elif utilisation_pivot == 'variable':
        valeur_duree = compl_2b_valeur_pivot()
        type_duree = compl_2c_type_pivot()
        delta_duree = relativedelta(days=+0)
        if type_duree == 'jour':
            delta_duree = relativedelta(days=+valeur_duree)
        elif type_duree == 'mois':
            delta_duree = relativedelta(months=+valeur_duree)
        else:
            res = False
            information = 'Type de durée de pivot invalide : %s' % type_duree
            ajouter_info(information)
            return res, date_decla, date_decla_max, information, avertissement, erreur, desc_delai_decla

        delta_franchise = (fin_franchise - debut_arret_travail).days + 1
        if delta_franchise < delta_duree.days:
            declaration_quantite = compl_2d_delai_declaration_avant_pivot()
            declaration_definition = compl_2e_delai_declaration_avant_pivot_definition()
        else:
            declaration_quantite = compl_2f_delai_declaration_apres_pivot()
            declaration_definition = compl_2g_delai_declaration_apres_pivot_definition()
    else:
        res = False
        message = 'Mode de délai de déclaration invalide %s' % utilisation_pivot
        information, erreur = message, message
        ajouter_info(information)
        return res, date_decla, date_decla_max, delta_decla, information, avertissement, erreur, desc_delai_decla

    desc_delai_decla += '\tType de délai de déclaration ? %s\n' % utilisation_pivot
    desc_delai_decla += '\tDebut arret travail : %s\n' % formater_date(debut_arret_travail)
    desc_delai_decla += '\tDélai de déclaration : %s %s\n' % (declaration_quantite, declaration_definition)

    ########################
    # DELAI DE DECLARATION #
    ########################

    date_decla = date_declaration_sinistre()
    date_decla_max = ajouter_jours(debut_arret_travail, 1)
    if 'jour_apres_arret_travail' in declaration_definition:
        date_decla_max = ajouter_jours(debut_arret_travail, declaration_quantite)
    elif 'mois_apres_arret_travail' in declaration_definition:
        date_decla_max = ajouter_mois(debut_arret_travail, declaration_quantite)
    elif 'jour_apres_franchise' in declaration_definition:
        date_decla_max = ajouter_jours(fin_franchise, declaration_quantite)
    elif 'mois_apres_franchise' in declaration_definition:
        date_decla_max = ajouter_mois(fin_franchise, declaration_quantite)
    elif 'sans_limite' in declaration_definition:
        date_decla_max = datetime.date(9999,12,31)
    else:
        res = False
        message = 'Définition de délai de déclaration invalide %s' % declaration_definition
        information, erreur = message, message
        ajouter_info(message)
        return res, date_decla, date_decla_max, delta_decla, information, avertissement, erreur, desc_delai_decla

    '''
    # DESACTIVE JC en attente de relecture
    if 'minimum_fin_franchise_et_' in declaration_definition:
        date_max_declaration = min(date_max_declaration, fin_franchise)
    '''

    delta_decla = (date_decla - date_decla_max).days + 1
    if date_decla > date_decla_max:
        if 'accord_de_prise_en_charge_declaration_hors_delai' not in documents_recus():
            res = False
            message = 'La date de déclaration saisie %s est superieure à la date maximale de déclaration %s.' \
                          % (formater_date(date_decla), formater_date(date_decla_max))
            message += '\nUn accord de prise en charge est nécessaire pour continuer.'
            information = message
            ajouter_info(message)
            return res, date_decla, date_decla_max, delta_decla, information, avertissement, erreur, desc_delai_decla

        desc_delai_decla += '\tDélai de déclaration (ok) : %s (déclaration) < %s (déclaration max)\n' % (
            formater_date(date_decla), formater_date(date_decla_max))

    message_debug(desc_delai_decla)
    return res, date_decla, date_decla_max, delta_decla, information, avertissement, erreur, desc_delai_decla


def gestion_delai_declaration():
    date_fin_franchise_initiale = param_date_fin_franchise_initiale()
    return rule_gestion_delai_declaration(date_fin_franchise_initiale=date_fin_franchise_initiale)

return gestion_delai_declaration() # DECOMMENTER SOUS COOG


#################################
# FIN GESTION DELAI DECLARATION #
