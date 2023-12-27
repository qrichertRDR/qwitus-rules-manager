# ---
# Name: Franchise selon un nombre de jours d'arrêt standard
# Short Name: fr_jours_arret_standard
# Type: tool
# ---

# DEBUT FR JOURS ARRET STANDARD #
#################################

#######################
# DEBUT GESTION MOTIF #
#######################

def gestion_motif(evenement,
                  franchise_accident,
                  franchise_accident_travail,
                  franchise_maladie,
                  franchise_maladie_pro,
                  franchise_maternite):

    dict_franchise_selon_motif = {
        'accident': franchise_accident,
        'accident_du_travail': franchise_accident_travail,
        'maladie': franchise_maladie,
        'maladie_professionnelle': franchise_maladie_pro,
        'maternite': franchise_maternite
    }

    message = 'Motif invalide : %s.' % evenement

    res = dict_franchise_selon_motif.get(evenement, message)

    if res is None:
        res = message

    if isinstance(res, str):
        ajouter_avertissement(res)
        ajouter_erreur(res)
        return
    return res

#####################
# FIN GESTION MOTIF #
#####################


########################
# DEBUT GESTION RACHAT #
########################

def gestion_rachat(evenement, condition_rachat, franchise_hors_rachat, franchise_rachat, jours_hospi):
        # TODO erreur aucun ou aucune ?
        # TODO simplifier cette condition si inutile
        # TODO permettre la saisie de nombres
        if condition_rachat == 'aucune':  # PAS DE RACHAT DE FRANCHISE
            return franchise_hors_rachat  # False
        else:  # RACHAT DE FRANCHISE
            # Franchise en rachat selon une condition
            dict_rachat = {
                'aucune': False,
                'acc': evenement in ['accident'],
                'act': evenement in ['accident_du_travail'],
                'hp1': jours_hospi >= 1,
                'hp2': jours_hospi >= 2,
                'hp3': jours_hospi >= 3,
                'hp4': jours_hospi >= 4,
                'hp5': jours_hospi >= 5,
                'hp6': jours_hospi >= 6,
                'hp7': jours_hospi >= 7,
                'hp15': jours_hospi >= 15,
                'hp30': jours_hospi >= 30,
                'ha3':
                    evenement == 'accident' and jours_hospi >= 3,
            }
            if dict_rachat.get(condition_rachat):
                return franchise_rachat
            else:
                return franchise_hors_rachat

######################
# FIN GESTION RACHAT #
######################


####################################
# DEBUT GESTION FRANCHISE UTILISEE #
####################################

def gestion_franchise_utilisee(debut, type_franchise):
    debut_annee_glissante = ajouter_jours(debut, -365)
    fin_annee_glissante = ajouter_jours(debut, -1)
    franchise_utilisee_cumulee_annee_glissante = nb_jour_franchise(debut_annee_glissante, fin_annee_glissante)

    debut_annee_civile = datetime.date(debut.year, 1, 1)
    fin_annee_civile = ajouter_jours(debut, -1)
    franchise_utilisee_cumulee_annee_civile = nb_jour_franchise(debut_annee_civile, fin_annee_civile)
    franchise_utilisee_continue = 0

    dict_franchise_utilisee = {
        'continue': franchise_utilisee_continue,
        'cumulee_annee_glissante': franchise_utilisee_cumulee_annee_glissante,
        'cumulee_annee_civile': franchise_utilisee_cumulee_annee_civile
    }

    res = dict_franchise_utilisee.get(type_franchise, 'Type de franchise_invalide : %s' % type_franchise)
    if isinstance(res, str):
        ajouter_erreur(res)
        return

    return res

##################################
# FIN GESTION FRANCHISE UTILISEE #
##################################


def fr_jours_arret_standard(gestion_declaration_tardive=True):
    return rule_fr_jours_arret_standard(
        a1_type_franchise=param_a1_type_franchise(),
        a2_franchise_accident=param_a2_franchise_accident(),
        a2a_condition_accident=param_a2a_condition_accident(),
        a2b_rachat_accident=param_a2b_rachat_accident(),
        a3_franchise_accident_travail=param_a3_franchise_accident_travail(),
        a3a_condition_accident_travail=param_a3a_condition_accident_travail(),
        a3b_rachat_accident_travail=param_a3b_rachat_accident_travail(),
        a4_franchise_maladie=param_a4_franchise_maladie(),
        a4a_condition_maladie=param_a4a_condition_maladie(),
        a4b_rachat_maladie=param_a4b_rachat_maladie(),
        a5_franchise_maladie_professionnelle=\
            param_a5_franchise_maladie_professionnelle(),
        a5a_condition_maladie_professionnelle=\
            param_a5a_condition_maladie_professionnelle(),
        a5b_rachat_maladie_professionnelle=\
            param_a5b_rachat_maladie_professionnelle(),
        a6_franchise_maternite=param_a6_franchise_maternite(),
        a6a_condition_maternite=param_a6a_condition_maternite(),
        a6b_rachat_maternite=param_a6b_rachat_maternite(),
        gestion_declaration_tardive=gestion_declaration_tardive
    )


# RETIRER PARAMETRES gestion_declaration_tardive SOUS COOG
def rule_fr_jours_arret_standard(
        a1_type_franchise, a2_franchise_accident, a2a_condition_accident,
        a2b_rachat_accident, a3_franchise_accident_travail,
        a3a_condition_accident_travail, a3b_rachat_accident_travail,
        a4_franchise_maladie, a4a_condition_maladie, a4b_rachat_maladie,
        a5_franchise_maladie_professionnelle,
        a5a_condition_maladie_professionnelle,
        a5b_rachat_maladie_professionnelle, a6_franchise_maternite,
        a6a_condition_maternite, a6b_rachat_maternite,
        gestion_declaration_tardive=True):
    '''
    :param param_a1_type_franchise: type de franchise
    :type param_a1_type_franchise: () -> str

    :param param_a2_franchise_accident: franchise en cas d'accident
    :type param_a2_franchise_accident: () -> int

    :param param_a3_franchise_accident_travail: franchise en cas d'accident du travail
    :type param_a3_franchise_accident_travail: () -> int

    :param param_a4_franchise_maladie: franchise en cas de maladie
    :type param_a4_franchise_maladie: () -> int

    :param param_a5_franchise_maladie_professionnelle: franchise en cas de maladie professionnelle
    :type param_a5_franchise_maladie_professionnelle: () -> int

    :param param_a6_franchise_maternite: franchise en cas de maternité
    :type param_a6_franchise_maternite: () -> int

    :return: date de fin de franchise calculée automatiquement selon le motif d'arrêt de travail
    :rtype: datetime
    '''

    # RECUPERATION DES PARAMETRES
    type_franchise = param_a1_type_franchise()

    franchise_accident = param_a2_franchise_accident()
    condition_accident = param_a2a_condition_accident()
    rachat_accident = param_a2b_rachat_accident()

    franchise_accident_travail = param_a3_franchise_accident_travail()
    condition_accident_travail = param_a3a_condition_accident_travail()
    rachat_accident_travail = param_a3b_rachat_accident_travail()

    franchise_maladie = param_a4_franchise_maladie()
    condition_maladie = param_a4a_condition_maladie()
    rachat_maladie = param_a4b_rachat_maladie()

    franchise_maladie_pro = param_a5_franchise_maladie_professionnelle()
    condition_maladie_pro = param_a5a_condition_maladie_professionnelle()
    rachat_maladie_pro = param_a5b_rachat_maladie_professionnelle()

    franchise_maternite = param_a6_franchise_maternite()
    condition_maternite = param_a6a_condition_maternite()
    rachat_maternite = param_a6b_rachat_maternite()

    # GESTION MOTIF IJ
    gestion_acc = compl_0a_gestion_accident()
    gestion_acc_tra = compl_0b_gestion_accident_du_travail()
    gestion_mal = compl_0c_gestion_maladie()
    gestion_mal_pro = compl_0d_gestion_maladie_professionnelle()
    gestion_mat = compl_0e_gestion_maternite()

    param_manquant = False
    param_manquant = (gestion_acc is not None and gestion_acc == True and (franchise_accident is None or condition_accident is None)) or \
                     (gestion_acc_tra is not None and gestion_acc_tra == True and (franchise_accident_travail is None or condition_accident_travail is None)) or \
                     (gestion_mal is not None and gestion_mal == True and (franchise_maladie is None or condition_maladie is None)) or \
                     (gestion_mal_pro is not None and gestion_mal_pro == True and (franchise_maladie_pro is None or condition_maladie_pro is None)) or \
                     (gestion_mat is not None and gestion_mat == True and (franchise_maternite is None or condition_maternite is None))

    date_erreur = datetime.date(9999, 1, 1)
    if param_manquant:
        message_param_manquant = 'Paramètre manquant sur la franchise automatique.'
        ajouter_info(message_param_manquant)
        ajouter_avertissement(message_param_manquant)
        ajouter_erreur(message_param_manquant)
        return date_erreur

    # CONTEXTE
    debut_prejudice = date_de_debut_du_prejudice()
    evenement = code_de_l_evenement_du_prejudice()
    jours_hospi = nombre_jours_hospitalisation_prejudice()
    rechute = est_une_rechute()

    labels = ["d'accident",
              "d'accident du travail",
              'de maladie',
              'de maladie professionnelle',
              'maternite']

    dict_fr = {
        'accident': (labels[0], franchise_accident, condition_accident, rachat_accident),
        'accident_du_travail': (labels[1], franchise_accident_travail, condition_accident_travail, rachat_accident_travail),
        'maladie': (labels[2], franchise_maladie, condition_maladie, rachat_maladie),
        'maladie_professionnelle': (labels[3], franchise_maladie_pro, condition_maladie_pro, rachat_maladie_pro),
        'maternite': (labels[4], franchise_maternite, condition_maternite, rachat_maternite)
    }

    # DESCRIPTION
    description = "\nFRANCHISE SELON UN NOMBRE DE JOURS D'ARRET\n"
    description += '\tType de franchise: %s\n' % type_franchise

    # for evenement in dict_fr:
    (label, franchise, condition, rachat) = dict_fr[evenement]

    description += '\tFranchise en cas %s : %s jours\n' % (label, franchise)
    description += '\tRachat en cas %s ? : %s\n' % (label, condition)
    description += '\tRachat en cas %s : %s jours\n' % (label, rachat)

    # RECHUTE
    if rechute:
        fin_franchise = ajouter_jours(debut_prejudice, -1)
        description += '\tAvec rechute : %s\n' % (formater_date(fin_franchise))
        description += '\tFin de franchise (en rechute) : %s\n' % (formater_date(fin_franchise))
        message_debug(description)
        return fin_franchise

    # DECLARATION TARDIVE
    if gestion_declaration_tardive and code_decision_eligibilite_prestation() == 'declaration_tardive_avec_penalite':
        decla_tardive_variable = compl_3a_declaration_tardive_variable()
        date_decla = date_declaration_sinistre()
        if decla_tardive_variable == 'sans_penalite':
            regle_decla_tardive = 'sans_penalite'
        elif decla_tardive_variable == 'fixe':
            regle_decla_tardive = compl_3b_penalite_decla_tardive_1()
        elif decla_tardive_variable == 'variable':
            regle_decla_tardive_1 = compl_3b_penalite_decla_tardive_1()
            delai_decla_tardive_1 = compl_3c_decla_tardive_delai_1()
            regle_decla_tardive_2 = compl_3d_penalite_decla_tardive_2()
            delai_decla_tardive_2 = compl_3e_decla_tardive_delai_2()
            fin_franchise_init = fr_jours_arret_standard(False) # éviter infinite recursion depth
            res, date_decla, date_decla_max, delta_decla, information, avertissement, erreur, description_delai_declaration = rule_gestion_delai_declaration(
                date_fin_franchise_initiale=fin_franchise_init)
            delai = delta_decla
            if delai <= delai_decla_tardive_1:
                regle_decla_tardive = 'sans_penalite'
            else:
                regle_decla_tardive = regle_decla_tardive_1
                if delai > delai_decla_tardive_2:
                    regle_decla_tardive = regle_decla_tardive_2
        else:
            regle_decla_tardive = 'erreur'  # générer erreur et sortir

        if regle_decla_tardive == 'sans_penalite':
            message = 'Règle de déclaration tardive (%s)' \
                      % (regle_decla_tardive)
            ajouter_info(message)
        elif regle_decla_tardive == 'date_decla':
            res = ajouter_jours(date_decla, -1)
            message = 'Règle de déclaration tardive (%s) : %s (dd)' \
                      % (regle_decla_tardive, formater_date(res))
            ajouter_info(message)
            return res
        elif regle_decla_tardive == 'date_decla_plus_franchise':
            debut_prejudice = date_decla
        # DEPLACER DANS ELIGIBILITE ? IMPOSSIBLE car eligibilité plus appellée
        elif regle_decla_tardive == 'max_date_decla_et_fin_franchise':
            # pass comportement dans franchise
            fin_franchise_init = fr_jours_arret_standard(False)  # infinite recursion depth
            res = max(date_decla, fin_franchise_init)
            # il faut recalculer sans appeler la fonction date_fin_franchise car la règle est rappelée.
            message = 'Règle de déclaration tardive (%s) : %s = max(%s (dd), %s (ff))' \
                      % (regle_decla_tardive, formater_date(res), formater_date(date_decla),
                         formater_date(fin_franchise_init))
            ajouter_info(message)
            return res
        elif regle_decla_tardive == 'refus':
            # pass comportement dans franchise
            res = datetime.date(9999, 1, 1)
            message = 'Règle de déclaration tardive (%s) : %s.' \
                      % (regle_decla_tardive, formater_date(res))
            ajouter_info(message)
            return res  # raise date value out of range car impossible de signaler autrement
            # sortir un message de texte ? non il faut obligatoirement sortir une date
            #  return datetime.date(9999,1,1) -> DEI 2/1/9999 il faut sortir une date particulière 1/1/9999 ?
        else:
            res = datetime.date(9999, 1, 2)
            message = 'Règle de déclaration tardive incorrecte (%s) : %s' \
                      % (regle_decla_tardive, formater_date(res))
            ajouter_erreur(message)
            # datetime.date.max raises date value out of range
            return res

    debut = debut_prejudice

    # FRANCHISE HORS RACHAT
    franchise_hors_rachat = gestion_motif(evenement=evenement,
                                          franchise_accident=franchise_accident,
                                          franchise_accident_travail=franchise_accident_travail,
                                          franchise_maladie=franchise_maladie,
                                          franchise_maladie_pro=franchise_maladie_pro,
                                          franchise_maternite=franchise_maternite)
    if franchise_hors_rachat is None:
        return date_erreur

    # FRANCHISE RETENUE (AVEC OU SANS RACHAT)
    evenement = code_de_l_evenement_du_prejudice()
    franchise = gestion_rachat(evenement=evenement,
                               condition_rachat=condition,
                               franchise_hors_rachat=franchise_hors_rachat,
                               franchise_rachat=rachat,
                               jours_hospi=jours_hospi)

    # FRANCHISE UTILISEE
    franchise_utilisee = gestion_franchise_utilisee(debut, type_franchise)
    if franchise_utilisee is None:
        return None

    # FRANCHISE RESTANTE
    franchise_restante = franchise - franchise_utilisee

    # FIN DE FRANCHISE
    fin_franchise = ajouter_jours(debut_prejudice, franchise_restante - 1)

    description += '\tSans rechute\n'
    description += '\tEvenement : %s\n' %evenement
    description += '\tFranchise hors rachat : %s\n' % franchise_hors_rachat
    description += '\tFranchise retenue : %s\n' % franchise
    description += '\tFranchise utilisée : %s\n' % franchise_utilisee
    description += '\tFranchise restante : %s\n' % franchise_restante
    description += '\tFin de franchise : %s\n' % formater_date(fin_franchise)

    message_debug(description)


    return fin_franchise

return fr_jours_arret_standard() # DECOMMENTER SOUS COOG

###############################
# FIN FR JOURS ARRET STANDARD #
