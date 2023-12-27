# ---
# Name: Indemnité Journalière standard
# Short Name: ij_salaire_standard
# Type: tool
# ---

# DEBUT IJ STANDARD #
#####################

# Méthodes d'aide au calcul
caractere_separateur_tranches = '/'
# caractere_separateur_classes = '$'
# caractere_separateur_inf_sup = ':'

####################################
# DEBUT IJ PALIER X MOTIF X ENFANT #
####################################

############################
# DEBUT IJ PALIER X ENFANT #
############################

######################
# DEBUT IJ CLASSIQUE #
######################

#####################
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
# DEBUT IJ STANDARD #
#####################

###################
# FIN IJ MANUELLE #
###################

####################
# FIN IJ CLASSIQUE #
####################

##########################
# FIN IJ PALIER X ENFANT #
##########################

##################################
# FIN IJ PALIER X MOTIF X ENFANT #
##################################

################
# FIN IJ MOTIF #
################

#################
# FIN IJ ENFANT #
#################

#########################
# FIN IJ MOTIF X ENFANT #
#########################


avertissements = []


def stocker_avertissement(message):
    avertissements.append(message)


def avertir(message, lever_avertissement=True):
    message = 'Garantie exercée %i, le %s.\n\n%s' % (
        champs_technique('service.id'),
        date_debut_periode_indemnisation(),
        message)
    if lever_avertissement:
        ajouter_avertissement(message)
    else:
        stocker_avertissement(message)


##########################
# FIN IJ PALIER STANDARD #
##########################

#########################
# FIN IJ PALIER X MOTIF #
#########################


def chaine_vers_taux(element, label):
    if isinstance(element, str):
        if element.count(caractere_separateur_tranches) == 2:
            pourcentages_str = element.split(caractere_separateur_tranches)
            pourcentages = [Decimal(x) for x in pourcentages_str]
            return pourcentages
        else:
            message = '%s incorrects : %s' % (label, element)
            message += '\nLe format est le suivant %TA/%TB/%TC.'
            return {'erreur': message}
    return element


def affiche_tranches(tranches, pcts=None):
    return affiche_liste(liste_a_afficher=tranches,
                         prefixe='T',
                         unite='€',
                         liste_limitante=pcts)


def affiche_pcts(pcts, tranches=None):
    return affiche_liste(liste_a_afficher=pcts,
                         prefixe='T',
                         unite='%',
                         liste_limitante=tranches)


def affiche_liste(liste_a_afficher, prefixe, unite, liste_limitante=None):
    description = ''
    if len(liste_a_afficher) > 0:
        description = ''
        lettre_depart = 'A'
        elem_2 = None
        for index, elem_1 in enumerate(liste_a_afficher):
            if liste_limitante is not None:
                elem_2 = liste_limitante[index]
            if elem_1 == 0 or elem_2 == 0:
                if index == 0:
                    return ''
                break
            if index > 0:
                description += ', '
            description += '%s%s %s%s' % (elem_1, unite, prefixe, lettre_depart)
            lettre_depart = chr(ord(lettre_depart) + 1)
        description += ''
    return description


###########################
# DEBUT IJ PALIER X MOTIF #
###########################

############################
# DEBUT IJ PALIER STANDARD #
############################


def vers_liste_tranches(tranches_dict):
    liste_tranche = []
    lettre_depart = 'A'
    while True:
        cle = 'T' + lettre_depart
        if cle in tranches_dict:
            liste_tranche.append(tranches_dict[cle])
        else:
            break
        lettre_depart = chr(ord(lettre_depart) + 1)
    return liste_tranche


##########################
# FIN IJ PALIER STANDARD #
##########################

#########################
# FIN IJ PALIER X MOTIF #
#########################


def tranches_sans_avec(base):
    # TRANCHES DE SALAIRE SANS OU AVEC PRIME
    brut_sans_prime_a = tranche_salaire(['gross_salary'])
    brut_avec_prime_a = tranche_salaire(['gross_salary',
                                         'salary_bonus'])

    net_sans_prime_a = tranche_salaire(['net_salary'])
    net_avec_prime_a = tranche_salaire(['net_salary',
                                        'net_salary_bonus'])
    switch_tranche = {
        'brut': (brut_sans_prime_a, brut_avec_prime_a),
        'net': (net_sans_prime_a, net_avec_prime_a)
    }

    res = switch_tranche.get(base, 'Type de salaire invalide : %s' % base)
    if isinstance(res, str):
        return {'erreur': res}

    tranches_sans_dict, tranches_avec_dict = res
    tranches_base_sans = vers_liste_tranches(tranches_sans_dict)
    tranches_base_avec = vers_liste_tranches(tranches_avec_dict)

    return tranches_base_sans, tranches_base_avec


def lim_prime(tranches_sans_prime, tranches_avec_prime, coef_lim_prime=0, precision=0.01):
    def description_lim_prime(
            tranches_sans, tranches_avec, coef, somme_sans=None, somme_avec=None,
            prime_max=None, prime_act=None, delta=None):

        if coef == -1:
            return '\nTranches (avec prime) : %s' % affiche_tranches(tranches_avec)

        if coef == -2:
            return '\nTranches (sans prime) : %s' % affiche_tranches(tranches_sans)

        desc = '\nLIMITATION DE LA PRIME A %s%%\n' % str(coef * 100)
        desc += 'Tranches (sans prime) : %s\n' % affiche_tranches(tranches_sans)
        desc += 'Tranches (avec prime) : %s\n' % affiche_tranches(tranches_avec)
        desc += 'Salaire (sans prime) : %.2f€\n' % somme_sans
        desc += 'Salaire (avec prime) : %.2f€\n' % somme_avec
        desc += 'Prime autorisée : %.2f€\n' % prime_max
        desc += 'Prime actuelle : %.2f€\n' % prime_act
        desc += '\n'

        # réduire de la prime actuelle - la prime maximum autorisée
        if delta > 0:
            desc += 'Réduire la prime de %.2f€\n' % delta
            desc += 'Tranches limitées : %s\n' % affiche_tranches(tranches_avec)

        return desc

    tranches_sans_prime = [arrondir(x, precision) for x in tranches_sans_prime]
    tranches_avec_prime = [arrondir(x, precision) for x in tranches_avec_prime]
    coef_lim_prime = arrondir(coef_lim_prime, precision)

    if coef_lim_prime == -1:
        return tranches_avec_prime, description_lim_prime(tranches_sans_prime, tranches_avec_prime, coef_lim_prime)

    if coef_lim_prime == -2:
        return tranches_sans_prime, description_lim_prime(tranches_sans_prime, tranches_avec_prime, coef_lim_prime)

    somme_sans_prime = sum(tranches_sans_prime)
    somme_avec_prime = sum(tranches_avec_prime)

    somme_sans_prime = arrondir(somme_sans_prime, precision)
    somme_avec_prime = arrondir(somme_avec_prime, precision)

    prime_actuelle = somme_avec_prime - somme_sans_prime
    prime_maximale = coef_lim_prime * somme_sans_prime

    prime_actuelle = arrondir(prime_actuelle, precision)
    prime_maximale = arrondir(prime_maximale, precision)

    delta_prime = prime_actuelle - prime_maximale
    delta_prime = arrondir(delta_prime, precision)

    description = description_lim_prime(
        tranches_sans_prime, tranches_avec_prime, coef_lim_prime, somme_sans_prime, somme_avec_prime, prime_maximale,
        prime_actuelle, delta_prime)

    if delta_prime > 0:
        reduction_cumulee = 0
        for index, tranche_avec in reversed(list(enumerate(tranches_avec_prime))):
            car = chr(ord('a') + index).upper()
            if delta_prime == 0:
                break

            tmp = tranches_avec_prime[index] - delta_prime  # soustraction de delta prime
            tmp = arrondir(tmp, precision)

            if tmp >= 0:  # réduction de la tranche et delta restant nul
                reduction_tranche = delta_prime
                delta_prime = 0
                tranches_avec_prime[index] = tmp
            else:  # mise à 0 de la tranche et delta restant non nul
                reduction_tranche = delta_prime + tmp
                delta_prime = - tmp
                tranches_avec_prime[index] = 0

            reduction_cumulee += reduction_tranche
            if reduction_tranche != 0:
                description += 'Réduction tranche %s : %.2f€\n' % \
                               (car, reduction_tranche)

    return tranches_avec_prime, description


def tranches_lim_prime(reference_prime, tranches_sans, tranches_avec, precision=0.01):
    dict_coef = {
        'oui': Decimal(-1),  # tranches avec prime non limitée
        'max_30%': Decimal(0.3),  # tranches avec prime limitée à 30% du salaire annuel
        'max_1/12': Decimal(1 / 12),  # tranches avec prime limitée à 1/12 du salaire annuel
        'non': Decimal(-2)  # tranches sans prime
    }
    coef = dict_coef.get(reference_prime,
                         'Type de prime invalide : %s' % reference_prime)
    if isinstance(coef, str):
        return {'erreur': coef}

    coef = arrondir(coef, precision)
    tranches_lim, description = lim_prime(tranches_sans, tranches_avec, coef)
    return tranches_lim, description


###########################
# DEBUT IJ PALIER X MOTIF #
###########################

############################
# DEBUT IJ PALIER STANDARD #
############################


def reference(tranches, pcts,
              type='',
              label='',
              debut=None, fin=None, ind=None,
              freq=None, date_ref=None, prem_rv=None, nb_j=None,
              precision=0.01, nbj_par_an=365, periodes=None,
              base='jour'):

    # code d'origine
    def calculate_salary_range(salary, pmss):
        salary_range = {'TA': 0,
                        'TB': 0,
                        'TC': 0}

        salary_range['TA'] = min(pmss, salary)
        if salary > pmss:
            salary_range['TB'] = min(3 * pmss, salary - pmss)
            if salary > 4 * pmss:
                salary_range['TC'] = min(4 * pmss, salary - 4 * pmss)
        return salary_range

    def description_reference(trs, pcts, ref_a, ref_j, type, rv=False):
        desc = ''
        # desc += '\nTRAITEMENT '
        # + label
        # + '\n'
        # desc += 'Tranches : %s\n' % affiche_tranches(tranches, pcts)
        desc += 'Salaire %s%s (annuel) : %.2f€ (' % \
                (type,
                 ' revalorisé' if rv
                 else '',
                 ref_a)

        for i, tranche in enumerate(trs):
            if tranche > 0:
                car = chr(ord('a') + i).upper()
                if i > 0:
                    desc += ', '
                desc += '%.2f€ T%s' % (tranche, car)
        desc += ')'

        if base == 'jour':
            desc += '\nSalaire %s%s (journalier) : %.2f€ ' \
                    '= %.2f€ / %d jours\n' % \
                    (type,
                     ' revalorisé' if rv
                     else '',
                     ref_j,
                     ref_a,
                     nbj_par_an)
        else:
            desc += '\n'
        return desc

    # Salaires de référence journalier
    tranches_salaire = [arrondir(x, precision) if y > 0 else Decimal(0) for (x, y) in zip(tranches, pcts)]

    # Salaire référence
    ref_a = sum(t for t in tranches_salaire)
    ref_a = arrondir(ref_a, precision)

    ref_j = ref_a / nbj_par_an
    ref_j = arrondir(ref_j, precision)

    description_ref = description_reference(trs=tranches_salaire, pcts=pcts,
                                            ref_a=ref_a, ref_j=ref_j,
                                            type=type)

    # ref_rv_liste_j = list()
    ref_rv_liste_a = list()
    description_revalo = ''
    if ind is not None:
        description_revalo = '\nREVALORISATION\n'
        res_rv = rule_revalorisation_privee(debut=debut, fin=fin, indice=ind,
                                            date_reference=date_ref,
                                            premiere_revalorisation=prem_rv,
                                            frequence=freq, nombre_jours=nb_j,
                                            montant_journalier=ref_a,
                                            inversion=False, periodes=periodes)

        if isinstance(res_rv, dict) and 'erreur' in res_rv:
            return {'erreur': res_rv['erreur']}

        ref_rv_liste_a, desc_revalo_a = res_rv
        description_revalo += desc_revalo_a

        # TODO lever l'hypothese de pmss stable sur une sous période de revalo

        # redécouper en fonction
        for reference_revalo_a in ref_rv_liste_a:
            # message_debug(reference_revalo_a)
            dsp = reference_revalo_a['start_date']
            # fsp = reference_revalo['end_date']

            ref_rv_a = reference_revalo_a['base_amount']
            ref_rv_j = arrondir(ref_rv_a / nbj_par_an, precision)

            reference_revalo_a['reference_a'] = ref_rv_a
            reference_revalo_a['reference_j'] = ref_rv_j

            pssa = table_pmss(dsp) * 12
            tranches = calculate_salary_range(ref_rv_a, pssa)
            tranches_liste = vers_liste_tranches(tranches)
            reference_revalo_a['tranches'] = tranches_liste

            reference_revalo_a['description_reference'] = description_reference(
                trs=tranches_liste, pcts=pcts, ref_a=ref_rv_a, ref_j=ref_rv_j,
                type=type, rv=True)

    return ref_j, ref_a, description_ref, description_revalo, ref_rv_liste_a


##########################
# FIN IJ PALIER STANDARD #
##########################

#########################
# FIN IJ PALIER X MOTIF #
#########################


def contractuel(tranches, pcts, label, liste_rv=None, precision=0.01, nbj_par_an=365, base='jour'):

    def description_contractuel(tranches, pcts, cont_a, cont_j, label):
        desc = ''
        desc += 'Salaire contractuel (annuel) : %.2f€ = ' % cont_a
        for i, tranche in enumerate(tranches):
            if tranche > 0:
                if i > 0:
                    desc += ' + '
                if pcts[i] == 100:
                    desc += '%.2f€' % tranche

                elif pcts[i] == 0:
                    pass
                else:
                    desc += '%.2f€ × %s%%' % (tranche, pcts[i])
        if base == 'jour':
            desc += '\nSalaire contractuel (journalier) : ' \
                    '%.2f€ = ' \
                    '%.2f€ ' \
                    '/ %d jours\n' % \
                    (cont_j, cont_a, nbj_par_an)
        else:
            desc += '\n'

        return desc

    def calcul(tranches, pcts, label):

        pcts_arr = [arrondir(x, precision) for x in pcts]
        tranches_arr = [arrondir(x, precision) for x in tranches]

        # Salaire contractuel
        pcts_x_tranches = [p * t / 100 for p, t in zip(pcts_arr, tranches_arr)]

        cont_a = sum(pcts_x_tranches)
        cont_a = arrondir(cont_a, precision)

        cont_j = cont_a / nbj_par_an
        cont_j = arrondir(cont_j, precision)

        desc_cont = description_contractuel(tranches_arr, pcts_arr, cont_a, cont_j, label)

        return cont_a, cont_j, desc_cont

    # Salaire contractuel
    cont_a, cont_j, desc_cont = calcul(tranches, pcts, label)
    if liste_rv is not None:
        for revalo in liste_rv:
            tranches = revalo['tranches']
            res_a, res_j, desc = calcul(tranches, pcts, label)

            # Modifier
            revalo['contractuel_a'] = res_a
            revalo['contractuel_j'] = res_j
            revalo['description_contractuel'] = desc
    else:
        liste_rv = list()
    return cont_j, cont_a, desc_cont, liste_rv


def description_prestation_journaliere(prestation_j):
    desc_j = '\nPRESTATION\n'
    desc_j += 'Prestation (journalière) : %.2f€' % prestation_j
    if prestation_j < 0:
        desc_j += ' soit %.2f€' % 0
    return desc_j


################################
# DEBUT IJSS CORRIGEE OU NULLE #
################################

def description_prestation_totale(prestation_j,
                                  nb_jours_prestation,
                                  prestation_t,
                                  type='ij',
                                  prestation_a=None):

    desc = '\nLa prestation réglée est de '
    if prestation_t == 0:
        desc += '%.2f€' % prestation_t
    elif prestation_t > 0:
        desc += '%.2f€ (%.2f€ × %s)' % (
        prestation_t, prestation_j, nb_jours_prestation)
    else:
        desc += '%.2f€ soit %.2f€' % (prestation_t, 0)
    return desc


def prestation_totale(prestation_j, dsp, fsp, precision=0.01): # IJ MANUELLE
    nb_jours_prestation = (fsp - dsp).days + 1
    prestation_t = prestation_j * nb_jours_prestation
    prestation_t = arrondir(prestation_t, precision)

    prestation_t = max(0, prestation_t)
    description = description_prestation_totale(prestation_j,
                                                nb_jours_prestation,
                                                prestation_t)
    return prestation_t, nb_jours_prestation, description

##############################
# FIN IJSS CORRIGEE OU NULLE #
##############################


def gestion_duree_max(label_duree, debut_arret_travail, date_fin_periode):
    # TODO retirer debut_arret_travail ?
    # TODO retirer date_fin_periode ?
    label = label_duree.upper()
    plus_365_jours = ajouter_jours(debut_arret_travail, 365)
    plus_1095_jours = ajouter_jours(debut_arret_travail, 1095)
    date_naissance = date_de_naissance()
    jusque_62_ans = ajouter_jours(ajouter_annees(date_naissance, 62), -1)
    jusque_65_ans = ajouter_jours(ajouter_annees(date_naissance, 65), -1)
    plus_1095_jours_ou_65_ans = min(plus_1095_jours, jusque_65_ans)
    fin_franchise = date_fin_franchise()
    plus_180_jours_ff = ajouter_jours(fin_franchise, 180)
    dei = ajouter_jours(fin_franchise, 1)
    plus_365_jours_dei = ajouter_jours(dei, 365)
    # DEBUT CCN
    plus_60_jours_dei = ajouter_jours(dei, 59)
    plus_80_jours_dei = ajouter_jours(dei, 79)
    plus_100_jours_dei = ajouter_jours(dei, 99)
    plus_120_jours_dei = ajouter_jours(dei, 119)
    plus_140_jours_dei = ajouter_jours(dei, 139)
    plus_160_jours_dei = ajouter_jours(dei, 159)
    plus_180_jours_dei = ajouter_jours(dei, 179)
    # FIN CCN
    plus_6_mois_dei = ajouter_mois(dei, 6)
    bloquant = True
    dict_indice = {
        '365_JOURS': (plus_365_jours,
                      'Limitation automatique à 365 jours '
                      "après le début d'arrêt de travail.",
                      bloquant),
        '365_JOURS_DEI': (plus_365_jours_dei,
                          'Limitation automatique à 365 jours '
                          "après le début d'indemnisation.",
                          bloquant),
        # DEBUT CCN
        '60_JOURS_DEI': (plus_60_jours_dei,
                         'Limitation automatique à 60 jours '
                         "après le début d'indemnisation.",
                         bloquant),
        '80_JOURS_DEI': (plus_80_jours_dei,
                         'Limitation automatique à 80 jours '
                         "après le début d'indemnisation.",
                         bloquant),
        '100_JOURS_DEI': (plus_100_jours_dei,
                          'Limitation automatique à 100 jours '
                          "après le début d'indemnisation.",
                          bloquant),
        '120_JOURS_DEI': (plus_120_jours_dei,
                          'Limitation automatique à 120 jours '
                          "après le début d'indemnisation.",
                          bloquant),
        '140_JOURS_DEI': (plus_140_jours_dei,
                          'Limitation automatique à 140 jours '
                          "après le début d'indemnisation.",
                          bloquant),
        '160_JOURS_DEI': (plus_160_jours_dei,
                          'Limitation automatique à 160 jours '
                          "après le début d'indemnisation.",
                          bloquant),
        # FIN CCN
        '180_JOURS_DEI': (plus_180_jours_dei,
                          'Limitation automatique à 180 jours '
                          "après le début d'indemnisation.",
                          bloquant),
        '180_JOURS_FF': (plus_180_jours_ff,
                          'Limitation automatique à 180 jours '
                          "après la fin de franchise.",
                          bloquant),
        '6_MOIS_DEI': (plus_6_mois_dei,
                       'Limitation automatique à 6 mois '
                       "après le début d'indemnisation.",
                       bloquant),
        '1095_JOURS': (plus_1095_jours,
                       'Limitation automatique à 1095 jours '
                       "après le début d'arrêt de travail.",
                       bloquant),
        '62_ANS': (jusque_62_ans,
                   "Limitation automatique aux 62 ans de l'assuré.",
                   bloquant),
        '65_ANS': (jusque_65_ans,
                   "Limitation automatique aux 65 ans de l'assuré.",
                   bloquant),
        '1095_JOURS_OU_65_ANS': (plus_1095_jours_ou_65_ans,
                                 'Limitation automatique à 1095 jours '
                                 "après le début d'arrêt de travail "
                                 "ou aux 65 ans de l'assuré.",
                                 bloquant),
        '62_ANS_NON_BLOQUANT': (jusque_62_ans,
                                "Limitation manuelle aux 62 ans de l'assuré.",
                                not bloquant),
        '62_ANS_OU_RETRAITE_NON_BLOQUANT': (jusque_62_ans,
                                "Limitation manuelle aux 62 ans de l'assuré "
                                'ou au départ à la retraite.',
                                not bloquant),
        'AUCUNE_LIMITE': (date_fin_periode,
                          'Pas de limitation de durée.',
                          not bloquant),
    }
    res_a, res_b, res_c = dict_indice.get(
        label,
        (None, 'Durée maximum de prestation invalide : %s\n' % label, None)
    )
    if res_a is None:
        return {'erreur': res_b}

    return res_a, res_b, res_c


def rv_prestation(debut, fin, indice, freq, date_ref, prem_revalo, nb_j,
                  deduction, cont_j, iss_plein_j, ib_j, p_j, mt_j=0,
                  iss_part_j=None, ib_red_j=None, mt_type=None, mt_lim_j=None,
                  est_rv_lim_mt=False, rup=False, lim_rup_j=None,
                  est_rv_lim_rup=False, precision=0.01, periodes=None):

    description_revalo = ''
    # ATTENTION RV LIM MT ET RV PRESTA : MIN(IB REDUITE INITIALE (ib_reduite_0), MTT AVEC MAJ LIMITE INITIALE (mt_lim_0 -> mt_lim_i)

    res_rv_liste = list()
    if not rup and mt_j > 0 and mt_lim_j > 0 and est_rv_lim_mt:

        res_rv = rule_revalorisation_privee(debut=debut, fin=fin,
                                            indice=indice,
                                            date_reference=date_ref,
                                            premiere_revalorisation=prem_revalo,
                                            frequence=freq, nombre_jours=nb_j,
                                            montant_journalier=mt_lim_j,
                                            inversion=False, periodes=periodes)

        # TODO : utiliser recuperer_erreur
        if isinstance(res_rv, dict) and 'erreur' in res_rv:
            return {'erreur': res_rv['erreur']}

        res_rv_liste, _ = res_rv

        for lim_mt_rv in res_rv_liste:

            # IB REDUITE
            # MI-TEMPS THERAPEUTIQUE
            mt_lim_rv_j = lim_mt_rv['base_amount']
            lim_mt_rv['limite_mi_temps_revalorisee_j'] = mt_lim_rv_j
            description_revalo += '\nREVALORISATION LIMITE MI-TEMPS'
            description_revalo += lim_mt_rv['description']

            mtt_rv_j, desc_mtt_rv_j = mi_temps_therapeutique(mt_lim_rv_j, iss_part_j, mt_j, mt_type, est_rv_lim_mt)
            description_revalo += desc_mtt_rv_j

            lim_mt_rv['mi_temps_therapeutique_revalorise_j'] = mtt_rv_j

            # PRESTATION APRES CUMUL
            p_rv_j, desc_cumul = cumul(mtt_rv_j, ib_red_j)
            description_revalo += desc_cumul

            description_revalo += '\nREVALORISATION PRESTATION'
            taux = lim_mt_rv['taux']
            res = arrondir(p_rv_j * taux, precision)
            lim_mt_rv['prestation_revalorisee_j'] = res
            description_revalo += '\nTaux : %.4f' % taux
            description_revalo += '\nLe montant revalorisé est de %.2f€\n' % res
            lim_mt_rv['description_prestation_revalorisee'] = description_revalo

    elif rup and lim_rup_j and lim_rup_j > 0 and est_rv_lim_rup:
        description_revalo += ''

        res_rv = rule_revalorisation_privee(debut=debut, fin=fin,
                                            indice=indice,
                                            date_reference=date_ref,
                                            premiere_revalorisation=prem_revalo,
                                            frequence=freq, nombre_jours=nb_j,
                                            montant_journalier=lim_rup_j,
                                            inversion=False, periodes=periodes)

        # TODO : utiliser recuperer_erreur
        if isinstance(res_rv, dict) and 'erreur' in res_rv:
            return {'erreur': res_rv['erreur']}

        res_rv_liste, _ = res_rv

        for lim_rup_rv in res_rv_liste:
            lim_rup_rv_j = lim_rup_rv['base_amount']
            if deduction:
                ib_lim_rup_rv_j = lim_rup_rv_j - iss_plein_j
            else:
                ib_lim_rup_rv_j = min(lim_rup_rv_j - iss_plein_j, cont_j)

            p_j = min(ib_j, ib_lim_rup_rv_j)
            description_revalo += '\nRECALCUL CUMUL APRES RUPTURE'
            description_revalo += '\nRègle de cumul : %.2f€ ' \
                                  '= min(' \
                                  '%.2f (indemnité base), ' \
                                  '%.2f (indemnité rup. rv)' \
                                  ')\n ' % \
                                  (p_j, ib_j, ib_lim_rup_rv_j)
            taux = lim_rup_rv['taux']

            res = p_j * taux
            description_revalo += '\nREVALORISATION PRESTATION'
            description_revalo += '\nTaux %.4f' % taux
            description_revalo += '\nLe montant revalorisé est de %.2f€\n' % res
            lim_rup_rv['prestation_revalorisee_j'] = res
            lim_rup_rv['description_prestation_revalorisee'] = description_revalo
    else:

        res_rv = rule_revalorisation_privee(debut=debut, fin=fin,
                                            indice=indice,
                                            date_reference=date_ref,
                                            premiere_revalorisation=prem_revalo,
                                            frequence=freq, nombre_jours=nb_j,
                                            montant_journalier=p_j,
                                            inversion=False, periodes=periodes)

        # TODO : utiliser recuperer_erreur
        if isinstance(res_rv, dict) and 'erreur' in res_rv:
            return {'erreur': res_rv['erreur']}

        res_rv_liste, _ = res_rv

        for presta_rv in res_rv_liste:
            presta_rv['prestation_revalorisee_j'] = \
                presta_rv['base_amount']
            if presta_rv['base_amount'] > 0:
                presta_rv['description_prestation_revalorisee'] = \
                    '\nREVALORISATION PRESTATION' \
                    + presta_rv['description']
            else:
                presta_rv['description_prestation_revalorisee'] = \
                    presta_rv['description']

    return res_rv_liste


#########################################
# FIN PARTIE COMMUNE IJ/RI A FACTORISER #
#########################################


###################
# FIN RI STANDARD #
###################


#################
# FIN RI ENFANT #
#################


def desc_iss_plein():
    desc = "IJSS temps plein"
    if param_convertir_ijss_brut_vers_net() and \
            compl_taux_conversion_ijss_brut_vers_net():
        desc += " nette"
    return desc


def desc_iss_partiel():
    desc = "IJSS mi-temps"
    if param_convertir_ijss_brut_vers_net() and \
            compl_taux_conversion_ijss_brut_vers_net():
        desc += " nette"
    return desc


def convert_ijss_brut_vers_net(ijss_brut, taux):
    cent = Decimal(100)
    zero = Decimal(0)
    ratio = max(zero, cent - taux) / cent
    ijss_net = arrondir(ijss_brut * ratio, 0.01)
    return ijss_net


def retabli(montant_j, label, liste_rv=None, precision=0.01):

    def description_retabli(montant_j, label):

        desc = '\nRETABLI ' \
               + label \
               + '\n'
        desc_cont = 'Salaire rétabli (journalier) : %.2f€ = ' % montant_j
        desc += desc_cont
        return desc

    def calcul(montant_j, label):

        # Salaire rétabli
        montant_j = arrondir(montant_j, precision)
        desc_ret = description_retabli(montant_j, label)

        return montant_j, desc_ret

    # Salaire contractuel
    ret_j, desc_ret = calcul(montant_j, label)

    if liste_rv is not None:
        for revalo in liste_rv:

            # Modifier
            taux = revalo['taux']
            res = ret_j * taux
            ret_rv_j, desc = calcul(res, label)
            revalo['retabli_j'] = ret_rv_j
            revalo['description_retabli'] = desc
    else:
        liste_rv = list()
    return ret_j, desc_ret, liste_rv


# DEBUT IJ
def indemnite_de_base(ref_j, cont_j, iss_plein_j, en_deduction, maintien_j, type_deduction_recccn, label='',
                      liste_rv=None, precision=0.01):

    def description_indemnite_base(ref_j, cont_j, ib_j):
        desc = '\nindemnité '.upper() \
               + label \
               + '\n'
        desc += 'Indemnité de base (journalière) : '

        # SALAIRE MAINTENU RELAIS COMPLEMENT CCN
        if maintien_j > 0 and type_deduction_recccn == 'max_ijss_sal':
            desc_ded_j = 'max(%.2f€ (maintien), %.2f€ (%s))' % \
                         (maintien_j, iss_plein_j, desc_iss_plein())
        else:
            desc_ded_j = '%.2f€ (%s)' % (iss_plein_j, desc_iss_plein())

        if en_deduction:
            desc += '%.2f€ = %.2f€ (contractuel) - %s\n' % \
                    (ib_j, cont_j, desc_ded_j)
        else:
            desc += '%.2f€ = ' \
                    'min(' \
                    '%.2f (traitement) - %s, ' \
                    '%.2f (contractuel)' \
                    ')\n' % \
                    (ib_j, ref_j, desc_ded_j, cont_j)
        return desc

    def description_revalo_taux(ib_j, taux, ib_rv_j):
        desc = '\nindemnité de base\n'.upper()
        desc += 'Indemnité de base revalorisée (journalière) : %.2f€ = ' \
                '%.2f€ ' \
                '× %.4f' % \
                (ib_rv_j, ib_j, taux)
        return desc

    def calcul(ref_j, cont_j):

        # SALAIRE MAINTENU RELAIS COMPLEMENT CCN
        if maintien_j > 0 and type_deduction_recccn == 'max_ijss_sal':
            deduction_j = max(iss_plein_j, maintien_j)
        else:
            deduction_j = iss_plein_j

        if en_deduction:
            ib_j = cont_j - deduction_j
        else:
            ib_j = min(ref_j - deduction_j, cont_j)

        ib_j = arrondir(ib_j, precision)
        description = description_indemnite_base(
            ref_j=ref_j, cont_j=cont_j, ib_j=ib_j
        )
        return ib_j, description

    # Indemnité de base
    ib_j, desc_ib = calcul(ref_j=ref_j, cont_j=cont_j)
    if liste_rv is not None:
        for rv in liste_rv:
            # Revalo traitement
            ref_j = rv['reference_j']
            cont_j = rv['contractuel_j']
            res, desc = calcul(ref_j, cont_j)
            rv['indemnite_base_j'] = res
            rv['description_indemnite_base_j'] = desc
    return ib_j, desc_ib, liste_rv


def indemnite_base_reduite(ib_j, reduction_ib, iss_plein_j, iss_mj, precision=0.01):
    reduction_ib = reduction_ib.upper()
    ib_j = arrondir(ib_j, precision)
    iss_plein_j = arrondir(iss_plein_j, precision)

    # FIX NH7
    if reduction_ib == 'PROPORTION_SS':

        if iss_plein_j == 0 or iss_mj == 0:
            message_erreur = ''

            if iss_plein_j == 0:
                message_erreur += 'IJSS avant mi-temps à zéro.\n'

            if iss_mj == 0:
                message_erreur += 'IJSS de mi-temps à zéro.\n'

            message_erreur += 'Impossible de calculer la réduction en proportions SS.'
            message_erreur += '\nMerci de saisir une indemnité corrigée.'

            return {'erreur': message_erreur}

    proportion_ss = iss_plein_j / iss_mj
    proportion_2 = 2
    dict_reduction = {
        'REDUCTION_50%': proportion_2,
        'PROPORTION_SS': proportion_ss,
        'INDEMNITE_BASE': 1
    }

    taux = dict_reduction.get(
        reduction_ib, 'Réduction IB invalide : %s' % reduction_ib
    )
    if isinstance(taux, str):
        return {'erreur': taux}

    # taux = arrondir(taux, precision)
    ib_reduite_j = ib_j / taux
    ib_reduite_j = arrondir(ib_reduite_j, precision)

    description = ''
    if taux != 1:
        description += 'Indemnité de base réduite (journalière) : '
        description += '%.2f€ = %.2f (indemnité de base) / %.4f (taux de réduction)\n' % (ib_reduite_j, ib_j, taux)

    return ib_reduite_j, description


def mi_temps_type_lim(type_lim, ref_rv_j, cont_rv_j, ret_rv_j):
    dict_lim = {
        'reference': ref_rv_j,
        'contractuel': cont_rv_j,  # tranches avec prime limitée
        'retabli' : ret_rv_j
    }
    lim = dict_lim.get(
        type_lim,
        'Type de lim de mi-temps thérapeutique invalide : %s' % type_lim
    )
    if isinstance(lim, str):
        return {'erreur': lim}

    return lim


def mi_temps_therapeutique(ref_j, iss_mt_j, mt_j, mt_type, est_rv_lim, precision=0.01):

    def description_mi_temps_therapeutique(mtt_j):
        desc_ref = 'traitement' \
            if mt_type == 'reference' \
            else 'contractuel'
        desc_ref += ' revalorisé' \
            if est_rv_lim == True \
            else ''
        desc = '\nMI-TEMPS THERAPEUTIQUE\n'
        desc += 'Mi-temps thérapeutique (journalier) : '
        desc += '%.2f€ = ' \
                '%.2f€ (%s) ' \
                '- %.2f€ (%s) ' \
                '- %.2f€ (salaire mi-temps)\n' % \
                (mtt_j, ref_j, desc_ref, iss_mt_j, desc_iss_partiel(), mt_j)

        return desc

    mtt_j = ref_j - iss_mt_j - mt_j
    mtt_j = arrondir(mtt_j, precision)

    return mtt_j, description_mi_temps_therapeutique(mtt_j)


def cumul(mtt_j, ib_reduite_j, precision=0.01):
    def description_cumul(mtt_j, ibr_j, p_j):
        desc = '\nCUMUL MI-TEMPS\n'
        desc += 'Cumul : %.2f€ = ' \
                'min(' \
                '%.2f€ (mi-temps therapeutique), ' \
                '%.2f€ (indemnité de base)' \
                ')\n' % (p_j, mtt_j, ibr_j)
        return desc

    mtt_j = arrondir(mtt_j, precision)
    ib_reduite_j = arrondir(ib_reduite_j, precision)

    prestation_j = min(mtt_j, ib_reduite_j)
    prestation_j = arrondir(prestation_j, precision)

    description = description_cumul(mtt_j, ib_reduite_j, prestation_j)

    return prestation_j, description


def prestation(ref0_j, cont0_j, ret0_j, iss_plein_j, ib0_j, rv_liste_base,
               mt_j=0, iss_part_j=None, mt_meth=None, mt_type=None,
               est_rv_lim_mt=False, rup=False, lim_rup=None, est_rv_lim_rup=False, ib_lim_rup0_j=None,
               rv_liste_lim_rup=None):

    def calcul(ref_rv_j=None, cont_rv_j=None, ret_rv_j=None, ib_rv_j=None, ib_lim_rup_rv_j=None):

        desc = ''
        description_ibr = ''
        description_mtt = ''
        description_cumul = ''
        rv_traitement = ref_rv_j is not None
        ib_reduite_j, mtl_j, mtt_j = None, None, None
        prestation_j = ib_rv_j if rv_traitement else ib0_j

        message_debug('**PH**'+';'+lim_rup)

        if not rup: # AVANT RUPTURE
            message_debug("avant rupture")
            if lim_rup not in ['', 'non']: # LIMITATION AVANT
            
                ibRVj_or_IB0j = ib_rv_j if rv_traitement and est_rv_lim_rup else ib0_j
                lim_ibrvj_or_limrupOj = ib_lim_rup_rv_j if rv_traitement and est_rv_lim_rup else ib_lim_rup0_j
                
                message_debug("======== Input du Minimum ========")
                message_debug("ibRVj_or_IB0j var: " + str(ibRVj_or_IB0j))
                message_debug("lim_ibrvj_or_limrupOj var: " + str(lim_ibrvj_or_limrupOj))
                message_debug("======== CONDITION ========")
                message_debug("rv_traitement: " + str(rv_traitement))
                message_debug("est_rv_lim_rup: " + str(est_rv_lim_rup))
                message_debug("rv_traitement and est_rv_lim_rup: " + str(rv_traitement and est_rv_lim_rup))
                message_debug("========= RESULTAT CONDITION =======")
                message_debug("si condition true ib_lim_rup_rv_j: " + str(ib_lim_rup_rv_j))
                message_debug("si condition false ib_lim_rup0_j: " + str(ib_lim_rup0_j))
              
                
                
                prestation_j = min(ibRVj_or_IB0j, lim_ibrvj_or_limrupOj)
            
            if mt_j != 0: # MI-TEMPS

                # IB REDUITE
                res_ibr = indemnite_base_reduite(
                    prestation_j , mt_meth, iss_plein_j, iss_part_j)
                message_erreur = recuperer_erreur(res_ibr)

                if message_erreur:
                    return {'erreur': message_erreur}

                ib_reduite_j, description_ibr = res_ibr
                desc += description_ibr

                # MI-TEMPS THERAPEUTIQUE
                mtl_j = mi_temps_type_lim(
                    mt_type,
                    ref_rv_j if rv_traitement and est_rv_lim_mt else ref0_j,
                    cont_rv_j if rv_traitement and est_rv_lim_mt else cont0_j,
                    ret_rv_j if rv_traitement and est_rv_lim_mt else ret0_j)
                message_erreur = recuperer_erreur(mtl_j)

                if message_erreur:
                    return {'erreur': message_erreur}

                mtt_j, description_mtt = mi_temps_therapeutique(
                    ref_j=mtl_j, iss_mt_j=iss_part_j, mt_j=mt_j, mt_type=mt_type,
                    est_rv_lim=rv_traitement and est_rv_lim_mt)
                desc += description_mtt

                # PRESTATION APRES CUMUL
                prestation_j, description_cumul = cumul(mtt_j, ib_reduite_j)
                
                desc += description_cumul
                message_debug("avant rupture fin")
        else: # APRES RUPTURE
            message_debug("Cas apèrs rupture")
            if lim_rup not in ['',
                               'non']: # LIMITATION APRES RUPTURE

                prestation_j = min(ib_rv_j if rv_traitement and est_rv_lim_rup else ib0_j,
                                   ib_lim_rup_rv_j if rv_traitement and est_rv_lim_rup else ib_lim_rup0_j)
                description_cumul = '\ncumul après rupture\n'.upper()
                description_cumul += 'Règle de cumul : %.2f€ ' \
                                     '= min(' \
                                     '%.2f (indemnité base), ' \
                                     '%.2f (indemnité rup.)' \
                                     ')\n ' % \
                        (prestation_j, ib_rv_j if rv_traitement and est_rv_lim_rup else ib0_j,
                         ib_lim_rup_rv_j if rv_traitement and est_rv_lim_rup else ib_lim_rup0_j)
                desc += description_cumul
        message_debug("fin de fonction")
        return ib_reduite_j, mtl_j, mtt_j, prestation_j, desc, description_ibr, description_mtt, description_cumul

    # FIX NH7
    res_calcul = calcul()
    message_erreur = recuperer_erreur(res_calcul)

    if message_erreur:
        return {'erreur': message_erreur}

    ibr0_j, mt_lim0_j, mtt0_j, p0_j, description, description_ibr, description_mtt, description_cumul = res_calcul

    # FAIRE CE QUI SUIT EN CAS DE REVALO ASSIETTE ?
    for i, rv in enumerate(rv_liste_base):
    
        ref_j = rv['reference_j']
        cont_j = rv['contractuel_j']
        ret_j = rv['retabli_j']
        ib_j = rv['indemnite_base_j']

        # AVANT RUPTURE
        if not rup:
            
            if lim_rup in ['', 'non']:
                pass
            
            
            #FIX 19/04/23 RECETTE SALVATORE REGLE MUTUALISE
            #rv_lim_rup = rv_liste_lim_rup[i]
            #ib_lim_rup_j = rv_lim_rup['indemnite_base_j']

            # FIX NH7
            #FIX 19/04/23 RECETTE SALVATORE REGLE MUTUALISE
            #res_calcul = calcul(ref_rv_j=ref_j, cont_rv_j=cont_j, ret_rv_j=ret_j, ib_rv_j=ib_j, ib_lim_rup_rv_j=ib_lim_rup_j)
            
            #FIX 19/04/23 RECETTE SALVATORE REGLE MUTUALISE
            res_calcul = calcul(ref_rv_j=ref_j, cont_rv_j=cont_j,
                                ret_rv_j=ret_j, ib_rv_j=ib_j)
            message_erreur = recuperer_erreur(res_calcul)

            if message_erreur:
                return {'erreur': message_erreur}

            ibr_j, mtl_j, mtt_j, p_j, desc, desc_ibr, desc_mtt, desc_cumul = res_calcul

            rv['prestation_j'] = p_j

            # MI TEMPS
            if mt_j > 0:
                rv['indemnite_base_reduite_j'] = ibr_j
                if est_rv_lim_mt:
                    rv['mi_temps_lim_j'] = mtl_j
                    rv['mi_temps_therapeutique_j'] = mtt_j

                    rv['description_limite_mi_temps_j'] = desc_mtt
                    rv['description_indemnite_reduite_j'] = desc_ibr
                    rv['description_cumul_j'] = desc_cumul
                    rv['description_prestation'] = desc
                else:
                    # REVALO TRAITEMENT et NON RV LIM MT : MIN(MTT INITIAL (mtt_0), IB REDUIT MAJ PROPAGATION (ibj_i))
                    res = min(mt_lim0_j, ibr_j)
                    desc_res_cumul = 'Prestation (journalière) %.2f€ = ' \
                                     'min(' \
                                     '%.2f€ (lim. mt), ' \
                                     '%.2f€ (ibr rv)' \
                                     ')' % (res, mt_lim0_j, ibr_j)
                    rv['prestation_j'] = res

                    rv['description_indemnite_reduite_j'] = desc_ibr
                    rv['description_limite_mi_temps_j'] = description_mtt
                    rv['description_cumul_j'] = desc_res_cumul
                    rv['description_prestation'] = desc_ibr + description_mtt + desc_cumul
        # APRES RUPTURE
        else:
            if lim_rup not in ['',
                               'non']:
                rv_lim_rup = rv_liste_lim_rup[i]
                ib_lim_rup_j = rv_lim_rup['indemnite_base_j']

                # FIX NH7
                res_calcul = calcul(ref_rv_j=ref_j, cont_rv_j=cont_j,
                                    ret_rv_j=ret_j, ib_rv_j=ib_j,
                                    ib_lim_rup_rv_j=ib_lim_rup_j)
                message_erreur = recuperer_erreur(res_calcul)

                if message_erreur:
                    return {'erreur': message_erreur}
                _, _, _, p_j, _, _, _, desc_cumul = res_calcul

                if est_rv_lim_rup:
                    rv['prestation_j'] = p_j # min(ib_lim_rup_j, ib_j)
                    rv['description_prestation'] = desc_cumul
                else:
                    res = min(ib_lim_rup0_j, ib_j)
                    desc_res_cumul = '\ncumul après rupture\n'.upper()
                    desc_res_cumul += 'Prestation (journalière) ' \
                                      '%.2f€ = ' \
                                      'min(' \
                                      '%.2f€ (indemnité rv), ' \
                                      '%.2f€ (indemnité rup.)' \
                                      ')\n' % \
                                      (res, ib_j, ib_lim_rup0_j)
                    rv['prestation_j'] = res
                    rv['description_prestation'] = desc_res_cumul

            else:  # cas du changement de base
                pass

    return ibr0_j, mt_lim0_j, mtt0_j, p0_j, description, rv_liste_base, description_ibr, description_mtt, description_cumul


# IJ
def ij_calcul(debut, fin, duree_max, en_deduction, prime_ref, base_av_rup, pcts_base_av_rup, lim_av_rup,
              pcts_lim_av_rup, revalo_lim_av_rup, mt_j, mt_lim, mt_reduction_ib, revalo_lim_mt, rup, base_ap_rup,
              pcts_base_ap_rup, lim_ap_rup, pcts_lim_ap_rup, revalo_lim_ap_rup, iss_plein_j, iss_partiel_j,
              iss_sanction_j, assiette, indice, freq, date_ref, prem_revalo, nb_j, retabli_j, maintenu_j, type_deduction_recccn):
    '''

    :param maintenu_j:
    :param type_deduction_recccn:
    :param lim_av_rup:
    :param pcts_lim_av_rup:
    :param revalo_lim_av_rup:
    :param retabli_j:
    :param debut: début de période de prestation
    :type debut: date

    :param fin: fin de période de prestation
    :type fin: date

    :param en_deduction: prestation en déduction
    :type en_deduction: bool

    :param base_av_rup: base de calcul avant rupture
    :type base_av_rup: str

    :param base_ap_rup: base de calcul après rupture
    :type base_ap_rup: str

    :param prime_ref: type de prime de référence
    :type prime_ref: str

    :param pcts_base_av_rup: pcts sur la base avant rupture
    :type pcts_base_av_rup: list[int]

    :param pcts_base_ap_rup: pcts sur la base après rup
    :type pcts_base_ap_rup: list[int]

    :param lim_ap_rup: lim de référence après rup
    :type lim_ap_rup: str

    :param pcts_lim_ap_rup: pcts sur la lim après rup
    :type pcts_lim_ap_rup: list[int]

    :param revalo_lim_ap_rup: revalorisaiton lim rup
    :type revalo_lim_ap_rup: str

    :param mt_lim: type de lim mi-temps
    :type mt_lim: str

    :param mt_reduction_ib: type de réduction mi-temps
    :type mt_reduction_ib: str

    :param revalo_lim_mt: revalorisation lim mi-temps
    :type revalo_lim_mt: str

    :param duree_max: durée maximale de prestation
    :type duree_max: str

    :param rup: sortie des effectifs ?
    :type rup: bool

    :param iss_plein_j: indemnité de sécurité sociale avant mi-temps
    :type iss_plein_j: Decimal

    :param iss_partiel_j: indemnité de sécurité sociale après mi-temps
    :type iss_partiel_j: Decimal

    :param iss_sanction_j: indemnité de sécurité sociale en cas de sanction
    :type iss_sanction_j: Decimal

    :param mt_j: salaie de temps partiel journalier
    :type mt_j: Decimal

    :param indice:
    :type indice: str

    :param freq:
    :type freq: str

    :param date_ref:
    :type date_ref: str

    :param prem_revalo:
    :type prem_revalo: str

    :param nb_j:
    :type nb_j: int

    :return:
    :rtype: list[dict[str,any]]
    '''

    dp, fp = debut, fin
    dat = date_debut_arret_de_travail()
    est_rv_lim_mt = revalo_lim_mt

    ###################################
    ########### DEBUT DEBUG ###########
    ###################################

    # CAS GENERAL
    desc_debug = '\nIJ SALAIRE TRANCHE\n'
    desc_debug += 'PERIODE : du %s au %s\n' % (formater_date(dp), formater_date(fp))
    desc_debug += '\nDurée max : %s\n' % duree_max

    res_gestion_duree_max = gestion_duree_max(duree_max, dat, fp)
    message_erreur = recuperer_erreur(res_gestion_duree_max)

    if message_erreur:
        return {'erreur': message_erreur}

    limite_fp, desc_limite_periode, bloquant = res_gestion_duree_max
    fp_min = min(fp, limite_fp)
    

    
    if fp_min < fp:
        if bloquant:
            fp = fp_min
            desc_debug += desc_limite_periode + ' : %s\n' % (formater_date(fp))
        else:
            message_avertissement = desc_limite_periode
            stocker_avertissement(message_avertissement)

    desc_debug += 'Prime : %s\n' % prime_ref
    desc_debug += 'En déduction : %s\n' % \
                  ('oui' if en_deduction
                   else 'non')
    desc_debug += 'Sortie des effectifs : %s\n' % \
                  ('oui' if rup
                   else 'non')

    desc_debug += '\nAssiette : %s\n' % assiette
    desc_debug += 'Indice : %s\n' % indice
    desc_debug += 'Fréquence : %s\n' % freq
    desc_debug += 'Date référence : %s\n' % date_ref
    desc_debug += 'Première revalorisation : %s\n' % \
                  (prem_revalo if nb_j is None
                   else ('+ '
                         + str(nb_j)
                         + ' jour(s)')
                   )

    desc_debug += '%s : %.2f€\n' % (desc_iss_plein(), iss_plein_j)

    # AVANT RUPTURE
    if not rup:

        # BASE
        if base_av_rup:
            desc_debug += '\nBase (avant rupture) : salaire %s\n' % \
                          base_av_rup
            desc_debug += '%% base (avant rupture) : %s\n' % \
                          affiche_pcts(pcts_base_av_rup)

        if type_deduction_recccn != 'sans_objet' and maintenu_j != 0:
            desc_debug += '\nSalaire maintenu : %.2f\n' % maintenu_j
            desc_debug += 'Type de déduction en relais complément ccn : %s\n' \
                          % type_deduction_recccn

        # LIMITE
        if lim_av_rup and lim_av_rup not in ['',
                                             'non']:
            message_avertissement = 'Limite avant rupture A VERIFIER.\n'
            #message_avertissement += "Par défaut, le calcul n'applique aucune limitation avant rupture."
            avertir(message_avertissement, False)
            #lim_av_rup = 'non'
            #revalo_lim_av_rup = False
            '''
            desc_debug += '\nLimite avant RUP : salaire %s\n' % lim_av_rup
            desc_debug += '%% lim avant RUP : %s\n' % affiche_pcts(pcts_lim_av_rup)
            desc_debug += 'Limite avant RUP revalorisée : %s\n' % 
            ('oui' if revalo_lim_av_rup 
            else 'non')
            '''
        # MI-TEMPS
        if mt_lim != '' and mt_j != 0:
            desc_debug += '\nSalaire (temps partiel) : %.2f€\n' % mt_j
            desc_debug += 'IJSS (temps partiel) : %.2f€\n' % iss_partiel_j
            desc_debug += 'Réduction IB : %s\n' % mt_reduction_ib
            desc_debug += 'Limite MT : %s\n' % mt_lim
            desc_debug += 'Limite MT revalorisée : %s\n' % \
                          ('oui' if est_rv_lim_mt
                           else 'non')
    # APRES RUPTURE
    else:
        # BASE
        desc_debug += '\nBase (après rupture) : salaire %s\n' % base_ap_rup
        desc_debug += '%% base (après rupture) : %s\n' % affiche_pcts(pcts_base_ap_rup)

        # LMITE
        if lim_ap_rup \
                and lim_ap_rup not in ['',
                                       'non']:
            desc_debug += '\nLimite après RUP : salaire %s\n' % lim_ap_rup
            desc_debug += '%% lim après RUP : %s\n' % affiche_pcts(pcts_lim_ap_rup)
            desc_debug += 'Limite après RUP revalorisée : %s\n' % \
                          ('oui' if revalo_lim_ap_rup
                           else 'non')

    if iss_sanction_j is not None and iss_sanction_j != 0:
        desc_debug += 'IJSS (sanction) : %.2f€\n' % iss_sanction_j

    # REFERENCE ET TAUX DE LA BASE DE CALCUL AVANT OU APRES RUPTURE
    res_tranches_sans_avec = tranches_sans_avec(base_ap_rup if rup else base_av_rup)
    message_erreur = recuperer_erreur(res_tranches_sans_avec)

    if message_erreur:
        return {'erreur': message_erreur}

    tranches_sans, tranches_avec = res_tranches_sans_avec

    pcts_base = pcts_base_ap_rup if rup else pcts_base_av_rup
    description = '\nPRESTATION APRES RUPTURE' \
        if rup \
        else '\nPRESTATION AVANT RUPTURE'
    desc_debug += description

    # PRIME (similaire pour le salaire de référence avant ou après rupture)
    res_tranches_lim_prime = tranches_lim_prime(
        prime_ref, tranches_sans, tranches_avec
    )
    message_erreur = recuperer_erreur(res_tranches_lim_prime)

    if message_erreur:
        return {'erreur': message_erreur}

    tranches, description = res_tranches_lim_prime
    desc_debug += '\nBASE ' + description

    #################################
    ########### FIN DEBUG ###########
    #################################


    #### DEBUT BASE ####

    # TRAITEMENT
    res_ref = reference(tranches=tranches, pcts=pcts_base, type=base_ap_rup if rup else base_av_rup, label='', debut=dp,
                        fin=fp, ind=indice, freq=freq, date_ref=date_ref,
                        prem_rv=prem_revalo, nb_j=nb_j)
    message_erreur = recuperer_erreur(res_ref)

    if message_erreur:
        return {'erreur': message_erreur}

    ref_j, _, desc_ref, _, rv_liste = res_ref

    # CONTRACTUEL
    cont_j, _, desc_cont, rv_liste = contractuel(
        tranches=tranches, pcts=pcts_base, label='', liste_rv=rv_liste
    )

    # RETABLI
    ret_j, desc_ret, rv_liste = retabli(
        montant_j=retabli_j, label='', liste_rv=rv_liste
    )

    # INDEMNITE DE BASE (DEDUCTION OU COMPLEMENT)
    ib_j, desc_ib, rv_liste = indemnite_de_base(ref_j=ref_j, cont_j=cont_j, iss_plein_j=iss_plein_j,
                                                en_deduction=en_deduction,
                                                maintien_j=maintenu_j, type_deduction_recccn=type_deduction_recccn,
                                                label='', liste_rv=rv_liste)

    #### FIN BASE ####

    #### DEBUT LIMITE APRES RUPTURE ####
    lim_rup = lim_ap_rup if rup else lim_av_rup
    pcts_lim_rup = pcts_lim_ap_rup if rup else pcts_lim_av_rup
    revalo_lim_rup = revalo_lim_ap_rup if rup else revalo_lim_av_rup
    label_rup = 'LIMITE après rupture' \
        if rup \
        else 'LIMITE avant rupture'
    ref_j_lim_rup, cont_j_lim_rup, ib_j_lim_rup, ib_lim_rup_rv_j, rv_liste_lim_rup = None, None, 0, 0, -1
    if lim_rup \
            and lim_rup not in ['',
                                'non']:

        # TRANCHE
        res_tranches_lim_rup_sans_avec = tranches_sans_avec(lim_rup)
        message_erreur = recuperer_erreur(res_tranches_lim_rup_sans_avec)

        if message_erreur:
            return {'erreur': message_erreur}

        tranches_lim_rup_sans, tranches_lim_rup_avec = res_tranches_lim_rup_sans_avec

        # PRIME
        res_tranches_lim_prime = tranches_lim_prime(
            prime_ref, tranches_lim_rup_sans, tranches_lim_rup_avec)
        message_erreur = recuperer_erreur(res_tranches_lim_prime)

        if message_erreur:
            return {'erreur': message_erreur}

        tranches_lim_rup, description = res_tranches_lim_prime
        desc_debug += '\n' + label_rup + description

        # TRAITEMENT
        res_ref = reference(
            tranches=tranches_lim_rup, type=lim_rup, pcts=pcts_lim_rup,
                            label=label_rup, debut=dp, fin=fp, ind=indice,
                            freq=freq, date_ref=date_ref, prem_rv=prem_revalo,
                            nb_j=nb_j)
        message_erreur = recuperer_erreur(res_ref)

        if message_erreur:
            return {'erreur': message_erreur}

        ref_j_lim_rup, _, desc_ref_lim_rup, _, rv_liste_lim_rup = res_ref

        # CONTRACTUEL
        cont_j_lim_rup, _, desc_cont_lim_rup, rv_liste_lim_rup = contractuel(
            tranches=tranches_lim_rup, pcts=pcts_lim_rup, label=label_rup,
            liste_rv=rv_liste_lim_rup
        )

        # TODO PK cont_j passé en paramètre dans ref_j et cont_j deux fois
        # INDEMNITE
        ib_j_lim_rup, desc_ib_lim_rup, rv_liste_lim_rup = indemnite_de_base(
            ref_j=ref_j_lim_rup, cont_j=cont_j_lim_rup, iss_plein_j=iss_plein_j, en_deduction=True,
            maintien_j=-1, type_deduction_recccn='',
            label=label_rup.upper(), liste_rv=rv_liste_lim_rup)


    #### FIN LIMITE RUPTURE ####

    desc_debug += '\n'
    desc_debug += '#'*80
    # message_debug(desc_debug)

    #  REVALO TRAITEMENT ATTENTION AU CAS 2 : MIN(MTT INITIAL (mtt_0), IB MAJ PROPAGATION (ibj_i))
    res_presta = prestation(
        ref0_j=ref_j, cont0_j=cont_j, ret0_j=ret_j, iss_plein_j=iss_plein_j, ib0_j=ib_j, rv_liste_base=rv_liste,
        mt_j=mt_j, iss_part_j=iss_partiel_j, mt_meth=mt_reduction_ib, mt_type=mt_lim, est_rv_lim_mt=est_rv_lim_mt,
        rup=rup, lim_rup=lim_rup, est_rv_lim_rup=revalo_lim_rup, ib_lim_rup0_j=ib_j_lim_rup, rv_liste_lim_rup=rv_liste_lim_rup
    )
    message_erreur = recuperer_erreur(res_presta)

    if message_erreur:
        return {'erreur': message_erreur}

    ib_reduite_j, mt_lim_j, mtt_j, p_j, desc_presta, rv_liste, desc_ibr, _, _ = res_presta

    #  REVALO PRESTA ATTENTION AU CAS 3 : MIN(IB REDUITE INITIALE (ib_reduite_0), MTT AVEC MAJ LIMITE INITIALE (mt_lim_0 -> mt_lim_i)
    if assiette == 'prestation':
        rv_liste = rv_prestation(debut=dp, fin=fp, indice=indice, freq=freq,
                                 date_ref=date_ref, prem_revalo=prem_revalo,
                                 nb_j=nb_j, deduction=en_deduction,
                                 cont_j=cont_j, iss_plein_j=iss_plein_j,
                                 ib_j=ib_j, p_j=p_j, mt_j=mt_j,
                                 iss_part_j=iss_partiel_j,
                                 ib_red_j=ib_reduite_j, mt_type=mt_lim,
                                 mt_lim_j=mt_lim_j,
                                 est_rv_lim_mt=est_rv_lim_mt, rup=rup,
                                 lim_rup_j=cont_j_lim_rup,
                                 est_rv_lim_rup=revalo_lim_rup)  #IB J LIM RUP -> CONT_J LIM RUP

        message_erreur = recuperer_erreur(rv_liste)

        if message_erreur:
            return {'erreur': message_erreur}

    res = []
    num_sous_periode = 1
    for i, rv in enumerate(rv_liste):
        desc_p = ''
        dsp = rv['start_date']
        fsp = rv['end_date']

        ref_rv_j =  -1
        cont_rv_j = -1
        ib_rv_j = -1

        ib_reduite_rv_j = -1
        lim_mt_rv_j = -1
        mtt_rv_j = -1

        lim_rup_rv_j = -1
        ib_lim_rup_rv_j = -1

        if assiette == 'prestation':  # PRESTATION
            desc_pr_v = rv['description_prestation_revalorisee']
            p_j_i = rv['prestation_revalorisee_j']
            if rup:  # APRES RUPTURE
                if revalo_lim_ap_rup:
                    lim_rup_rv_j = rv_liste_lim_rup[i]['contractuel_j']
                    ib_lim_rup_rv_j = rv_liste_lim_rup[i]['indemnite_base_j']

                    # DESCRIPTION
                    desc_ref_lim_rup = rv_liste_lim_rup[i][
                        'description_reference']
                    desc_cont_lim_rup = rv_liste_lim_rup[i][
                        'description_contractuel']
                    desc_ib_lim_rup = rv_liste_lim_rup[i][
                        'description_indemnite_base_j']

                    desc_presta = '' # TEST

            else:  # AVANT RUPTURE

                if revalo_lim_av_rup:
                    lim_rup_rv_j = rv_liste_lim_rup[i]['contractuel_j']
                    ib_lim_rup_rv_j = rv_liste_lim_rup[i]['indemnite_base_j']

                if mt_j > 0:  # APRES MI-TEMPS
                    if est_rv_lim_mt:
                        lim_mt_rv_j = rv['limite_mi_temps_revalorisee_j']
                        mtt_rv_j = rv['mi_temps_therapeutique_revalorise_j']

                        desc_presta = desc_ibr

        else:  # TRAITEMENT
            ref_rv_j = rv['reference_j']
            cont_rv_j = rv['contractuel_j']
            ib_rv_j = rv['indemnite_base_j']

            # DESCRIPTION
            desc_ref = rv['description_reference']
            desc_cont = rv['description_contractuel']
            desc_ret = rv['description_retabli']
            desc_ib = rv['description_indemnite_base_j']

            p_j_i = rv['prestation_j'] # indemnite_base_revalo_j
            if rup:# APRES RUPTURE
                if revalo_lim_ap_rup:
                    lim_rup_rv_j = rv_liste_lim_rup[i]['contractuel_j']
                    ib_lim_rup_rv_j = rv_liste_lim_rup[i]['indemnite_base_j']

                    # DESCRIPTION
                    desc_ref_lim_rup = rv_liste_lim_rup[i][
                        'description_reference']
                    desc_cont_lim_rup = rv_liste_lim_rup[i][
                        'description_contractuel']
                    desc_ib_lim_rup = rv_liste_lim_rup[i][
                        'description_indemnite_base_j']

                desc_presta = rv['description_prestation']

            else:  # AVANT RUPTURE
                if revalo_lim_av_rup:
                    lim_rup_rv_j = rv_liste_lim_rup[i]['contractuel_j']
                    ib_lim_rup_rv_j = rv_liste_lim_rup[i]['indemnite_base_j']

                    # DESCRIPTION
                    desc_ref_lim_rup = rv_liste_lim_rup[i][
                        'description_reference']
                    desc_cont_lim_rup = rv_liste_lim_rup[i][
                        'description_contractuel']
                    desc_ib_lim_rup = rv_liste_lim_rup[i][
                        'description_indemnite_base_j']

                if mt_j > 0: # APRES MI-TEMPS
                    ib_reduite_rv_j = rv['indemnite_base_reduite_j']

                    if est_rv_lim_mt:
                        lim_mt_rv_j = rv['mi_temps_lim_j']
                        mtt_rv_j = rv['mi_temps_therapeutique_j']

                    desc_presta = rv['description_prestation']

        # REFERENCE
        desc_p += 'TRAITEMENT\n'
        desc_p += desc_ref
        desc_p += desc_cont
        if retabli_j > 0:
            desc_p += desc_ret

        # IB
        desc_p += desc_ib

        if lim_rup \
                and lim_rup not in ['',
                                    'non']:
            # LIMITE
            desc_p += '\nTRAITEMENT %s\n' % label_rup.upper()
            desc_p += desc_ref_lim_rup
            desc_p += desc_cont_lim_rup

            # IB LIMITE
            desc_p += desc_ib_lim_rup

        # IB REDUITE, MTT, CUMUL
        desc_p += desc_presta

        if assiette == 'prestation':
            desc_p += desc_pr_v

        # PRESTATION JOURNALIERE
        # desc_j = description_prestation_journaliere(prestation_j=p_j_i)
        # desc_p += desc_j
        p_j_i = max(0, p_j_i)

        # SORTIE CGT ASSUREUR AUCUN MAINTIEN AUCUNE REPRISE
        p_j, p_j_i, desc_cgt = rule_cgt_partage_prestation(debut_periode=dsp,
                                                           base_courante=p_j,
                                                           base_reva_courante=p_j_i)

        desc_p += desc_cgt

        # PRESTATION TOTALE
        prestation_t, nb_jours_prestation, description = prestation_totale(
            p_j_i, dsp, fsp
        )
        desc_p += description

        str_num_sous_periode = str(num_sous_periode)

        # CAS GENERAL
        test_p = {
            'erreur': 0,
            # NON REVALO
            'reference_j': ref_j,
            'contractuel_j': cont_j,
            'indemnite_base_j': ib_j,
            'prestation_j': p_j,
            'prestation_rv_j': 0,
            # REVALO TEST SET 1
            'prestation_j_' + str_num_sous_periode:
                p_j_i if assiette == 'traitement' else -1,
            # REVALO TEST SET 2
            'reference_revalorisee_j_' + str_num_sous_periode:
                ref_rv_j or -1,
            'contractuel_revalorise_j_' + str_num_sous_periode:
                cont_rv_j or -1,
            'indemnite_base_revalorisee_j_' + str_num_sous_periode:
                ib_rv_j or 0,
            'prestation_revalorisee_j_' + str_num_sous_periode:
                p_j_i if assiette == 'prestation' else -1,
            'prestation_totale_' + str_num_sous_periode: prestation_t,
        }

        if rup:  # APRES RUPTURE
            test_p['limite_rupture_j'] = cont_j_lim_rup or 0
            test_p['indemnite_base_rupture_j'] = ib_j_lim_rup
            # test_p['limite_rupture_j_' + str_num_sous_periode] = lim_rup_j
            test_p['limite_rupture_revalorisee_j_' + str_num_sous_periode] = \
                lim_rup_rv_j
            test_p['indemnite_base_rupture_revalorisee_j_' + str_num_sous_periode] = \
                ib_lim_rup_rv_j
        else:  # AVANT RUPTURE
            if mt_j != 0:  # APRES MI-TEMPS
                # NON REVALO
                test_p['indemnite_base_reduite_j'] = ib_reduite_j
                test_p['limite_mi_temps_j'] = mt_lim_j
                test_p['mi_temps_therapeutique_j'] = mtt_j
                # REVALO
                test_p['indemnite_base_revalorisee_reduite_j_' + str_num_sous_periode] = \
                    ib_reduite_rv_j
                test_p['limite_mi_temps_revalorisee_j_' + str_num_sous_periode] = \
                    lim_mt_rv_j
                test_p['mi_temps_therapeutique_j_' + str_num_sous_periode] = \
                    mtt_rv_j

        res_p = {
            'start_date': dsp,
            'end_date': fsp,
            'nb_of_unit': nb_jours_prestation,
            'unit':
                'day',
            'amount': prestation_t,
            'base_amount': max(0, p_j),
            'amount_per_unit': max(0, p_j_i),
            'description': desc_p,
            'limit_date': None,
            'extra_details': {
                'tranche_a': str(tranches[0]),
                'tranche_b': str(tranches[1]),
                'tranche_c': str(tranches[2]),
                'ijss': str(iss_plein_j),
                'ijss_temps_partiel': str(iss_partiel_j),
                'sanction_ijss': str(iss_sanction_j),
            },
            'test_data': test_p
        }
        num_sous_periode = num_sous_periode + 1
        ajouter_info(desc_p)
        res.append(res_p)

    return res


##########################
# IDEMNITES JOURNALIERES #
##########################

def ij_standard():
    '''
    .. todo :: Externaliser dans un autre fichier
    '''
    duree = param_duree()
    en_complement = param_en_complement()
    prime = param_prime()
    base_av_rup = param_base_av_rup()
    pcts_base_av_rup = param_pcts_base_av_rup()
    lim_av_rup = param_lim_av_rup()
    pcts_lim_av_rup = param_pcts_lim_av_rup()
    rv_lim_av_rup = param_rv_lim_av_rup()
    base_ap_rup = param_base_ap_rup()
    pcts_base_ap_rup = param_pcts_base_ap_rup()
    lim_ap_rup = param_lim_ap_rup()
    pcts_lim_ap_rup = param_pcts_lim_ap_rup()
    rv_lim_ap_rup = param_rv_lim_ap_rup()
    red_ib_mt = param_red_ib_mt()
    lim_mt = param_lim_mt()
    rv_lim_mt = param_rv_lim_mt()
    assiette_rv = param_assiette_rv()
    freq_rv = param_freq_rv()
    indice_rv = param_indice_rv()
    premiere_rv = param_premiere_rv()
    date_ref_rv = param_date_ref_rv()
    nbj_rv = param_nbj_rv()
    convertir_ijss_brut_vers_net = param_convertir_ijss_brut_vers_net()
    type_deduction_recccn = param_type_deduction_recccn()
    debut = param_debut()
    fin = param_fin()

    return rule_ij_salaire_standard(
        duree=duree, en_complement=en_complement, prime=prime,
        base_av_rup=base_av_rup, pcts_base_av_rup=pcts_base_av_rup,
        lim_av_rup=lim_av_rup, pcts_lim_av_rup=pcts_lim_av_rup,
        rv_lim_av_rup=rv_lim_av_rup, base_ap_rup=base_ap_rup,
        pcts_base_ap_rup=pcts_base_ap_rup, lim_ap_rup=lim_ap_rup,
        pcts_lim_ap_rup=pcts_lim_ap_rup, rv_lim_ap_rup=rv_lim_ap_rup,
        red_ib_mt=red_ib_mt, lim_mt=lim_mt, rv_lim_mt=rv_lim_mt,
        assiette_rv=assiette_rv, freq_rv=freq_rv, indice_rv=indice_rv,
        premiere_rv=premiere_rv, date_ref_rv=date_ref_rv, nbj_rv=nbj_rv,
        convertir_ijss_brut_vers_net=convertir_ijss_brut_vers_net,
        type_deduction_recccn=type_deduction_recccn, debut=debut, fin=fin
    )

def rule_ij_salaire_standard(
        duree, en_complement, prime, base_av_rup, pcts_base_av_rup, lim_av_rup,
        pcts_lim_av_rup, rv_lim_av_rup, base_ap_rup, pcts_base_ap_rup,
        lim_ap_rup, pcts_lim_ap_rup, rv_lim_ap_rup, red_ib_mt, lim_mt,
        rv_lim_mt, assiette_rv, freq_rv, indice_rv, premiere_rv, date_ref_rv,
        nbj_rv, convertir_ijss_brut_vers_net, type_deduction_recccn, debut, fin
    ):

    '''
    :param debut:
    :param fin:
    :données complémentaires:
        - ijss
        - sanction_ijss
        - ib_corrigee
    :return:
    :rtype: list[dict[str,any]]
    '''

    ############
    # CONTEXTE #
    ############

    # PERIODE (debut, fin)
    dp = debut if debut is not None else date_debut_periode_indemnisation()
    fp = fin if fin is not None else date_fin_periode_indemnisation()

    # SALAIRES (brut, net)
    brut = salaire_brut()
    net = salaire_net()

    if brut is None:
        message_none = 'Salaire brut non renseigné.'
        return {'erreur': message_none}
    elif brut <= 0:
        message_brut = 'Salaire brut négatif ou nul.'
        avertir(message_brut, False)

    ##############
    # PARAMETRES #
    ##############

    # GENERAL (deduction)
    en_deduction = not en_complement

    # TESTS
    if en_complement is None:
        message_none = 'Calcul en déduction/complément non renseigné.'
        return {'erreur': message_none}

    #################
    # AVANT RUPTURE #
    #################

    rup = element_couvert_est_beneficiaire()

    # BASE
    if base_av_rup is None:
        message_none = 'Base avant rupture non renseignée.'
        return {'erreur': message_none}
    else:
        if not rup:
            if base_av_rup == 'net' and (net is None or (net is not None and net <= 0)):
                message_none = 'Net non renseigné pour le calcul avant rupture.'
                return {'erreur': message_none}

    # TAUX BASE
    if pcts_base_av_rup is None:
        message_none = 'Taux de base avant rupture non renseignés.'
        return {'erreur': message_none}
    else:
        label_pcts_base_av_rup = 'Taux de base avant rupture'
        pcts_base_av_rup = chaine_vers_taux(pcts_base_av_rup, label_pcts_base_av_rup)
        message_erreur = recuperer_erreur(pcts_base_av_rup)
        if message_erreur:
            return {'erreur': message_erreur}

    # LIMITE
    if lim_av_rup != 'non':
        if rup is not None and not rup:
            if lim_av_rup == 'net' \
                    and (net is None or (net is not None and net == 0)):
                message_none = 'Net non renseigné pour la limite avant rupture.'
                return {'erreur': message_none}

            if lim_av_rup == 'ajpe_net':
                message_none = 'Limite avant rupture : AJPE non implémenté.'
                return {'erreur': message_none}

        # TAUX LIMITE
        if pcts_lim_av_rup is None:
            message_none = 'Taux de limite avant rupture non renseignés.'
            return {'erreur': message_none}
        else:
            label_pcts_lim_av_rup = 'Taux de limite avant rupture'
            pcts_lim_av_rup = chaine_vers_taux(pcts_lim_av_rup, label_pcts_lim_av_rup)
            message_erreur = recuperer_erreur(pcts_lim_av_rup)
            if message_erreur:
                return {'erreur': message_erreur}

    #################
    # APRES RUPTURE #
    #################

    # BASE
    if base_ap_rup is None:
        message_none = 'Base après rupture non renseignée.'
        return {'erreur': message_none}
    else:
        if base_ap_rup in ['',
                           'idem']:
            base_ap_rup = base_av_rup
            pcts_base_ap_rup = pcts_base_av_rup
        if rup:
            if base_ap_rup == 'net' \
                    and (net is None or (net is not None and net == 0)):
                message_none = 'Net non renseigné pour le calcul après rupture.'
                return {'erreur': message_none}

    # TAUX BASE
    if pcts_base_ap_rup is None:
        message_none = 'Taux de base après rupture non renseignés.'
        return {'erreur': message_none}
    else:
        label_pcts_base_ap_rup = 'Taux de base après rupture'
        pcts_base_ap_rup = chaine_vers_taux(pcts_base_ap_rup, label_pcts_base_ap_rup)
        message_erreur = recuperer_erreur(pcts_base_ap_rup)
        if message_erreur:
            return {'erreur': message_erreur}

    # LIMITE
    if lim_ap_rup != 'non':
        if rup:
            if lim_ap_rup == 'net' and (net is None or (net is not None and net == 0)):
                message_none = 'Net non renseigné pour la limite après rupture'
                return {'erreur': message_none}

            if lim_ap_rup == 'ajpe_net':
                message_none = 'Limite après rupture : AJPE non implémenté.'
                return {'erreur': message_none}

        # TAUX LIMITE
        if pcts_lim_ap_rup is None:
            message_none = 'Taux de limite après rupture non renseignés.'
            return {'erreur': message_none}
        else:
            label_pcts_lim_ap_rup = 'Taux de limite après rupture'
            pcts_lim_ap_rup = chaine_vers_taux(pcts_lim_ap_rup, label_pcts_lim_ap_rup)
            message_erreur = recuperer_erreur(pcts_lim_ap_rup)
            if message_erreur:
                return {'erreur': message_erreur}

    ############
    # MI TEMPS #
    ############

    red_mt = red_ib_mt
    lim_mt = lim_mt
    revalo_lim_mt = rv_lim_mt
    salaire_retabli_j = montant_de_deduction('salaire_retabli', dp, fp)

    ###########
    # DONNEES #
    ###########

    iss_j = compl_ijss()
    iss_sanction_j = compl_sanction_ijss()

    # Salaire temps partiel
    iss_temps_plein_j = 0
    iss_temps_partiel_j = 0
    salaire_temps_partiel_j = montant_de_deduction('part_time', dp, fp)
    if salaire_temps_partiel_j > 0:
        # FIX NBO7

        if lim_mt == 'retabli':

            # AVEC BLOCAGE CAR NON IMPLEMENTE
            return {'erreur': 'Limite de mi-temps : salaire rétabli non implémenté.'}

        iss_temps_partiel_j = iss_j
        iss_av_mt_j = ijss_avant_mi_temps()
        if iss_av_mt_j is None:
            return {'erreur': 'Aucune ijss avant mi-temps trouvée. Merci de réaliser une prestation manuelle.'}
        iss_temps_plein_j = iss_av_mt_j
    else:
        iss_temps_plein_j = iss_j

    # Salaire maintenu ccn
    salaire_maintenu_j = montant_de_deduction('salaire_maintenu_ccn', dp, fp)

    # RELAIS COMPLEMENT CCN PARAMETRE
    if type_deduction_recccn is not None:
        # TYPES MAX_IJSS_SAL, IJSS
        if type_deduction_recccn in ['max_ijss_sal',
                                     'ijss']:
            message_avertissement = 'Ce contrat prévoit un relais complément ccn en déduction '
            if type_deduction_recccn == 'max_ijss_sal':
                message_avertissement += 'du maximum entre ijss et salaire maintenu.\n'
            elif type_deduction_recccn == 'ijss':
                message_avertissement += "de l'ijss.\n"

            # EXCLUSIONS (AVANT RUPTURE ET MI-TEMPS, APRES RUPTURE
            if rup:
                # DONE avertissement (pas d'application de la déduction ijss classique après rupture)
                message_avertissement += 'Après rupture, le relais complément ccn est sans objet.\n'
                type_deduction_recccn = 'sans_objet'
            else:
                if salaire_temps_partiel_j > 0:
                    # DONE avertissement (pas d'application de la déduction ijss classique avant rupture et après mi-temps)
                    message_avertissement += 'Avant rupture et avec mi-temps, le relais complément ccn est sans objet.\n'
                    type_deduction_recccn = 'sans_objet'
                else:
                    message_avertissement += 'Avant rupture et sans mi-temps, le relais complément ccn est pris en compte.\n'

                    if salaire_maintenu_j > 0:
                        message_avertissement += 'Un salaire maintenu est renseigné.\n'
                    else:
                        message_avertissement += "Aucun salaire maintenu n'est renseigné.\n"
            avertir(message_avertissement, False)
        # TYPE SANS OBJET
        elif type_deduction_recccn == 'sans_objet':
            pass
        # TYPE INVALIDE
        else:
            message_invalide = 'Type de relais complément ccn invalide : %s.' % type_deduction_recccn
            return {'erreur': message_invalide}
    # RELAIS COMPLEMETN CCN NON PARAMETRE
    else:
        message_none = 'Type de déduction en relais complément non paramétré.'
        return {'erreur': message_none}

    if convertir_ijss_brut_vers_net:
        tc_ijss_brut_net = compl_taux_conversion_ijss_brut_vers_net()
        if tc_ijss_brut_net is None:
            message_none = "Taux de conversion d'ijss brut vers net non renseigné"
            return {'erreur': message_none}

        iss_temps_plein_j = convert_ijss_brut_vers_net(iss_temps_plein_j, tc_ijss_brut_net)
        iss_temps_partiel_j = convert_ijss_brut_vers_net(iss_temps_partiel_j, tc_ijss_brut_net)

    results = ij_calcul(
        debut=dp, fin=fp, duree_max=duree, en_deduction=en_deduction,
        prime_ref=prime, base_av_rup=base_av_rup,
        pcts_base_av_rup=pcts_base_av_rup, lim_av_rup=lim_av_rup,
        pcts_lim_av_rup=pcts_lim_av_rup, revalo_lim_av_rup=rv_lim_av_rup,
        mt_j=salaire_temps_partiel_j, mt_lim=lim_mt, mt_reduction_ib=red_mt,
        revalo_lim_mt=revalo_lim_mt, rup=rup, base_ap_rup=base_ap_rup,
        pcts_base_ap_rup=pcts_base_ap_rup, lim_ap_rup=lim_ap_rup,
        pcts_lim_ap_rup=pcts_lim_ap_rup, revalo_lim_ap_rup=rv_lim_ap_rup,
        iss_plein_j=iss_temps_plein_j, iss_partiel_j=iss_temps_partiel_j,
        iss_sanction_j=iss_sanction_j, assiette=assiette_rv, indice=indice_rv,
        freq=freq_rv, date_ref=date_ref_rv, prem_revalo=premiere_rv,
        nb_j=nbj_rv, retabli_j=salaire_retabli_j,
        maintenu_j=salaire_maintenu_j,
        type_deduction_recccn=type_deduction_recccn
    )
    
    if len(avertissements) > 0 and len(results) > 0:
        results[0].setdefault('avertissements', avertissements)
    message_debug("Règle fini")
    return results
return ij_standard() # DECOMMENTER SOUS COOG

###################
# FIN IJ STANDARD #
