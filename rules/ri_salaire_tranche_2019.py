# ---
# Name: Rente classique (nouveau)
# Short Name: ri_salaire_tranche_2019
# Type: benefit
# ---

###########################################
# DEBUT PARTIE COMMUNE IJ/RI A FACTORISER #
###########################################

###########################
# DEBUT IJ PALIER X MOTIF #
###########################

############################
# DEBUT IJ PALIER STANDARD #
############################

###########################
# DEBUT IJ MOTIF X ENFANT #
###########################

###################
# DEBUT IJ ENFANT #
###################

##################
# DEBUT IJ MOTIF #
##################

######################
# DEBUT IJ CLASSIQUE #
######################

#####################
# DEBUT RI STANDARD #
#####################


# Méthodes d'aide au calcul
caractere_separateur_tranches = '/'
# caractere_separateur_classes = '$'
# caractere_separateur_inf_sup = ':'

def avertir(message):
    message = 'Garantie exercée %i, le %s.\n\n%s' % (
        champs_technique('service.id'),
        date_debut_periode_indemnisation(),
        message)
    ajouter_avertissement(message)


def chaine_vers_taux(element, label):
    if isinstance(element, str):
        if element.count(caractere_separateur_tranches) == 2:
            pourcentages_str = element.split(caractere_separateur_tranches)
            pourcentages = [Decimal(x) for x in pourcentages_str]
            return pourcentages
        else:
            message = '%s incorrects : %s' % (label, element)
            message += '\nLe format est le suivant %TA/%TB/%TC.'
            ajouter_erreur(message)
            return
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
        ajouter_erreur(res)
        return

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
        ajouter_erreur(coef)
        return

    coef = arrondir(coef, precision)
    tranches_lim, description = lim_prime(tranches_sans, tranches_avec, coef)
    return tranches_lim, description


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
            ajouter_erreur(res_rv['erreur'])
            return

        ref_rv_liste_a, desc_revalo_a = res_rv
        description_revalo += desc_revalo_a

        # TODO lever l'hypothese de pmss stable sur une sous période de revalo

        # redécouper en fonction
        for reference_revalo_a in ref_rv_liste_a:
            message_debug(reference_revalo_a)
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


#####################
# DEBUT IJ MANUELLE #
#####################


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


###################
# FIN IJ MANUELLE #
###################


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
    plus_180_jours_dei = ajouter_jours(dei, 180)
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
        (None, 'Durée maximum de prestation invalide : %s\n' % label)
    )
    if res_a is None:
        ajouter_erreur(res_b)
        return

    return res_a, res_b, res_c


def rv_prestation(debut, fin, indice, freq, date_ref, prem_revalo, nb_j,
                  deduction, cont_j, iss_plein_j, ib_j, p_j, mt_j=0,
                  iss_part_j=None, ib_red_j=None, mt_type=None, mt_lim_j=None,
                  est_rv_lim_mt=False, rup=False, lim_rup_j=None,
                  est_rv_lim_rup=False, precision=0.01, periodes=None):

    description_revalo = ''
    # ATTENTION RV LIM MT ET RV PRESTA : MIN(IB REDUITE INITIALE (ib_reduite_0), MTT AVEC MAJ LIMITE INITIALE (mt_lim_0 -> mt_lim_i)

    res_rv_liste = list()
    if rup and lim_rup_j and lim_rup_j > 0 and est_rv_lim_rup:
        description_revalo += ''

        res_rv = rule_revalorisation_privee(debut=debut, fin=fin,
                                            indice=indice,
                                            date_reference=date_ref,
                                            premiere_revalorisation=prem_revalo,
                                            frequence=freq, nombre_jours=nb_j,
                                            montant_journalier=lim_rup_j,
                                            inversion=False, periodes=periodes)

        if isinstance(res_rv, dict) and 'erreur' in res_rv:
            ajouter_erreur(res_rv['erreur'])
            return

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

        if isinstance(res_rv, dict) and 'erreur' in res_rv:
            ajouter_erreur(res_rv['erreur'])
            return

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


#####################
# DEBUT RI STANDARD #
#####################


def description_taux(base_ren, cat, cat_, tx_ren, tx_ren_remp):
    desc_taux = ''
    if '_r2' in base_ren:
        desc_taux += '\nTAUX (%s) : %s' % (
            cat_.upper(), affiche_pcts(tx_ren_remp)
        )
        if base_ren == 'X%_r2':
            desc_taux += '\nTAUX (%s) : %s%% de R2' % (
                cat.upper(),
                tx_ren[0]
            )
        else:
            desc_taux += '\nTAUX (%s) : %s de R2' % (
                cat.upper(),
                base_ren.split('_')[0]
            )
    else:
        desc_taux += '\nTAUX (%s) : %s' % (cat.upper(), affiche_pcts(tx_ren))
    return desc_taux


def switch_coef_r2(base, tip, tx_X):
    base = base.lower()

    # Correctif tip is none switch coef
    if tip is not None:
        tip /= Decimal(100)
    else:
        tip = Decimal(0)

    coef = 1
    tx_X /= Decimal(100)
    p_33 = Decimal(33) / Decimal(100)
    p_66 = Decimal(66.0) / Decimal(100)
    p_20 = Decimal(20.0) / Decimal(100)
    p_50 = Decimal(50.0) / Decimal(100)
    p_75 = Decimal(75.0) / Decimal(100)
    p_60 = Decimal(60.0) / Decimal(100)
    zero = Decimal(0)
    deux = Decimal(2)
    trois = Decimal(3)

    if base == '60%_r2':
        coef = p_60
    elif base == '75%_r2':
        coef = p_75
    elif base == 'x%_r2':
        coef = tx_X
    elif base == '3tip/2_r2':
        if tip < p_33:
            coef = zero
        elif p_33 <= tip < p_66:
            coef = trois * tip / deux
    elif base == 'tip/66%_r2':
        if tip < p_33:
            coef = zero
        elif p_33 <= tip < p_66:
            coef = tip / p_66
    elif base == '(tip-33%)/33%_r2':
        if tip < p_33:
            coef = zero
        elif p_33 <= tip < p_66:
            coef = tip - p_33 / p_33
    elif base == 'tip/50%_r2':
        if tip < p_20:
            coef = zero
        elif p_20 <= tip < p_50:
            coef = tip / p_50
    else:
        ajouter_erreur('Mode invalide de r2')
        return None

    return Decimal(str(coef))


def base_taux(cat, ren_1, ren_2, ren_3, ren_at, tx_ren_1, tx_ren_2, tx_ren_3,
              tx_ren_at, rss_ren_1, rss_ren_2, rss_ren_3, rss_ren_at, tx_lim_1,
              tx_lim_2, tx_lim_3, tx_lim_at, rss_lim_1, rss_lim_2, rss_lim_3,
              rss_lim_at, tip):

    def description_base_taux(cat, base, tx_ren, rss_ren, tx_lim, rss_lim):

        res = '\nCatégorie de rente : %s\n' % cat
        res += 'Base calcul : %s\n' % base
        if 'r2' not in base:
            res += 'Taux rente: %s\n' % affiche_pcts(tx_ren)
            res += 'RSS rente : %s\n' % rss_ren
            res += 'Taux lim.: %s\n' % affiche_pcts(tx_lim)
            res += 'RSS lim. : %s\n' % rss_lim
        else:
            if cat == 'rat':
                res += 'TIP : %s\n' % tip
            else:
                res += 'X : %s\n' % tx_ren[0]
        return res

    dict_mode_pourcentages = {
        'r1': (ren_1, tx_ren_1, rss_ren_1, tx_lim_1, rss_lim_1),
        'r2': (ren_2, tx_ren_2, rss_ren_2, tx_lim_2, rss_lim_2),
        'r3': (ren_3, tx_ren_3, rss_ren_3, tx_lim_3, rss_lim_3),
        'rat': (ren_at, tx_ren_at, rss_ren_at, tx_lim_at, rss_lim_at)
    }

    res = dict_mode_pourcentages.get(
        cat, 'Catégorie de rente invalide %s' % cat
    )

    if isinstance(res, str):
        ajouter_erreur(res)
        return

    base, taux_ren, rss_ren, taux_lim, rss_lim = res
    desc = description_base_taux(
        cat, base, taux_ren, rss_ren, taux_lim, rss_lim
    )
    return base, taux_ren, rss_ren, taux_lim, rss_lim, desc


# Gestion des proratas
def switch_prorata(type_prorata, nb_j, periodicite):
    # TODO prorata

    dict_jours_periode = {
        'mensuel': Decimal(30),
        'trimestriel': Decimal(90)
    }

    nb_j_periode = dict_jours_periode.get(
        periodicite, 'Periodicité invalide %s' % periodicite
    )

    if isinstance(nb_j_periode, str):
        ajouter_erreur(nb_j_periode)
        return

    dict_prorata = {
        'tout': 1,
        'rien': 0,
        'prorata': min(1, nb_j / nb_j_periode)
    }

    prorata = dict_prorata.get(
        type_prorata, 'Prorata invalide %s' % type_prorata
    )

    if isinstance(prorata, str):
        ajouter_erreur(prorata)
        return

    return prorata


# Gestion du mode de déduction TP
def switch_mode_deduction(mode_ded, cont_ded_a, ded_rss_a, ta, dp, fp,
                          liste_rv_ded, precision=0.01):

    def description_deduction(
            deductions_a, cont_ded_a, rss_percue_a, ded_rss_a, mode_ded, tp_a,
            ta, pe_a, ad_a
    ):

        desc_lim_a = '%.2f€' % cont_ded_a

        desc_rss_a = ''
        if rss_percue_a > 0:
            desc_rss_a = '- %.2f€' % rss_percue_a
        elif ded_rss_a > 0:
            desc_rss_a = '- %.2f€' % ded_rss_a

        desc_pe_a = ''
        if pe_a > 0:
            desc_pe_a = '- %.2f€' % pe_a

        desc_s_a = ''
        if mode_ded == 'saisi':
            if tp_a > 0:
                desc_s_a = '- %.2f€' % tp_a
        elif mode_ded == 'taux':
            if ta > 0 and cont_ded_a > 0:
                desc_s_a = '- %.2f%% × %.2f€' % \
                           (ta, cont_ded_a)

        desc_ad_a = ''
        if ad_a > 0:
            desc_ad_a = '- %.2f€' % ad_a

        desc_deduction = ''
        if deductions_a != cont_ded_a:
            desc_deduction += '\nDEDUCTION ANNUELLE'
            desc_deduction += '\n%.2f€ = %s %s %s %s %s' % (
                deductions_a, desc_lim_a, desc_rss_a, desc_s_a, desc_pe_a,
                desc_ad_a
            )

        return desc_deduction

    def calcul(cont_ded_a):

        # TODO selon cg

        # Nombre de jours par an pour les déductions
        nbj_an_ded = 365

        # salaire maintenu brut, net à payer, net imposable
        tp_brut_a = arrondir(
            montant_de_deduction('salaire_brut', dp, fp) * nbj_an_ded,
            precision
        )

        tp_net_pay_a = arrondir(
            montant_de_deduction('salaire_net_a_payer', dp, fp) * nbj_an_ded,
            precision
        )

        tp_net_imp_a = arrondir(
            montant_de_deduction('salaire_net_imposable', dp, fp) * nbj_an_ded,
            precision
        )

        tps = [tp_brut_a, tp_net_pay_a, tp_net_imp_a]
        tps_positif = [1 if x > 0 else 0 for x in tps]
        somme_tps_positif = sum(tps_positif)

        deductions_a = cont_ded_a

        rss_percue_a = arrondir(
            montant_de_deduction('rss_percue', dp, fp) * nbj_an_ded,
            precision
        )

        # REDMINE DIFFERENCIER LA PRESENCE D'UNE RSS renseignée à 0
        if rss_percue_a > 0:
            message = 'Une RSS perçue est utilisée dans les déductions.'
            ajouter_avertissement(message)
            deductions_a -= rss_percue_a
        else:
            deductions_a -= ded_rss_a

        tp_a = Decimal(0)
        if mode_ded == 'saisi':

            if ta is not None and ta > 0:
                message = "Dans le mode de déduction 'saisi', " \
                          "le taux d'activité n'est pas pris en compte."
                ajouter_avertissement(message)

            if somme_tps_positif == 0:
                message = 'Salaire maintenu non renseigné ou nul ' \
                          'dans les prestations annexes.'
                ajouter_avertissement(message)
                tp_a = Decimal(0)
            elif somme_tps_positif == 1:
                index_salaire = tps_positif.index(1)
                tp_a = tps[index_salaire]
            elif somme_tps_positif > 1:
                message = 'Renseigner un seul salaire maintenu ' \
                          'dans les prestations annexes.'
                ajouter_erreur(message)
                return None, ''

            deductions_a -= tp_a

        elif mode_ded == 'taux':

            if somme_tps_positif >= 1:
                message = "Dans le mode de déduction 'taux', " \
                          'le salaire saisi dans les prestations annexes ' \
                          "n'est pas pris en compte."
                ajouter_avertissement(message)

            if ta is None:
                message = "Le taux d'activité est non renseigné."
                ajouter_erreur(message)
                return None, ''
            else:
                if ta < 0:
                    message = "Le taux d'activité est négatif."
                    ajouter_erreur(message)
                    return None, ''
                elif ta == 0:
                    message = "Le taux d'activité renseigné est nul."
                    ajouter_avertissement(message)
                else:  # ta > 0:
                    deductions_a -= cont_ded_a * ta / Decimal(100)

        else:
            message = 'Mode de déduction invalide'
            ajouter_erreur(message)
            return None, ''

        # pole emploi
        pe_brut_a = arrondir(
            montant_de_deduction('pole_emploi_brut', dp, fp) * nbj_an_ded,
            precision
        )

        pe_simple_a = arrondir(
            montant_de_deduction('pole_emploi', dp, fp) * nbj_an_ded,
            precision
        )

        pe_net_a = arrondir(
            montant_de_deduction('pole_emploi_net', dp, fp) * nbj_an_ded,
            precision
        )

        pes = [pe_simple_a, pe_brut_a, pe_net_a]
        pes_positif = [1 if x > 0 else 0 for x in pes]
        somme_pes_positif = sum(pes_positif)

        pe_a = Decimal(0)
        if somme_pes_positif == 0:
            message = 'Aucune allocation pôle emploi renseignée ' \
                      'dans les prestations annexes.'
            ajouter_avertissement(message)
            pe_a = Decimal(0)
        elif somme_pes_positif == 1:
            index_pole_emploi = pes_positif.index(1)
            pe_a = pes[index_pole_emploi]
        elif somme_pes_positif > 1:
            message = 'Renseigner une seule allocation pôle emploi ' \
                      'dans les prestations annexes.'
            ajouter_erreur(message)
            return None, ''

        deductions_a -= pe_a

        # autres revenus
        ad_a = arrondir(
            montant_de_deduction('autres_revenus', dp, fp) * nbj_an_ded,
            precision
        )

        if ad_a == 0:
            message = 'Aucun autre revenu renseigné ' \
                      'dans les prestations annexes.'
            ajouter_avertissement(message)
        elif ad_a > 0:
            pass
        else:
            message = 'Montant de déduction négatif.'
            ajouter_erreur(message)
            return None, ''

        deductions_a -= ad_a

        desc_deduction = description_deduction(deductions_a=deductions_a,
                                               cont_ded_a=cont_ded_a,
                                               rss_percue_a=rss_percue_a,
                                               ded_rss_a=ded_rss_a,
                                               mode_ded=mode_ded, tp_a=tp_a,
                                               ta=ta, pe_a=pe_a, ad_a=ad_a)

        return deductions_a, desc_deduction

    ded_a, desc_ded_a = calcul(cont_ded_a=cont_ded_a)
    if ded_a is None:
        ajouter_erreur(desc_ded_a)
        return ded_a, desc_ded_a, []

    for rv_ded in liste_rv_ded:
        cont_ded_a_rv = rv_ded['contractuel_a']
        ded_a_i, desc_ded_a_i = calcul(cont_ded_a=cont_ded_a_rv)
        rv_ded['deduction_a'] = ded_a_i
        rv_ded['description_deduction_a'] = desc_ded_a_i

    return ded_a, desc_ded_a, liste_rv_ded


# Gestion du mode de déduction TP
def switch_rss_categorie_salaire(type_rss1, type_rss2, type_rss3,
                                 type_rssrat, rss1_n, rss1_b, rss2_n,
                                 rss2_b, rss3_n, rss3_b, rssat_n, rssat_b,
                                 cat):

    def description_rss_categorie_type(cat_rss, type_rss, ren_rss):
        desc = '\n%s (%s) : %.2f€' % \
               (type_rss.upper(), cat_rss.upper(), ren_rss)
        return desc

    dict_categorie_rss = {
        'r1': (
            type_rss1,
            {
                'brut': rss1_b,
                'net': rss1_n
            }
        ),
        'r2': (
            type_rss2,
            {
                'brut': rss2_b,
                'net': rss2_n
            }
        ),
        'r3': (
            type_rss3,
            {
                'brut': rss3_b,
                'net': rss3_n
            }
        ),
        'rat': (
            type_rssrat,
            {
                'brut': rssat_b,
                'net': rssat_n
            }
        )
    }

    # SELECTION PARMI R1, R2, R3, RAT
    res_cat = dict_categorie_rss.get(
        cat, 'Categorie de rente invalide %s' % cat
    )

    if isinstance(res_cat, str):
        ajouter_erreur(res_cat)
        return

    type_rss, dict_brut_ou_net = res_cat
    res_type = dict_brut_ou_net.get(
        type_rss, 'Type de rente invalide %s' % type_rss
    )

    if isinstance(res_type, str):
        ajouter_erreur(res_type)
        return

    desc = description_rss_categorie_type(cat_rss=cat, type_rss=type_rss,
                                          ren_rss=res_type)

    return type_rss, res_type, desc


def rente_de_base(cont_ren_a, cont_lim_a, ren_rss_a, lim_rss_a, en_deduction,
                  tx_X, base=None, tip=None, label='', liste_rv_ren=None,
                  liste_rv_lim=None, precision=0.01):

    def description_rente_base(
            cont_ren_a, cont_lim_a, rb_a, lb_a, rbl_a, coef
    ):

        desc = ''
        desc_rb = '\n\nRENTE ANNUELLE\n%.2f€ = ' % rb_a
        desc_lb = '\n\nLIMITE ANNUELLE\n%.2f€ = ' % lb_a
        desc_rbl = '\n\nLa rente annuelle hors déduction ' \
                   '(prestations annexes) est de %.2f€\n' \
                   % rbl_a

        if en_deduction:
            if '_r2' in base:
                desc_rb += '['

            desc_rb += '%.2f€ ' \
                       '- %.2f€' % (cont_ren_a, ren_rss_a)

            if '_r2' in base:
                desc_rb += ']'

            desc_lb += '%.2f€ ' \
                       '- %.2f€' % (cont_lim_a, lim_rss_a)
        else:
            if '_r2' in base:
                desc_rb += '['

            desc_rb += '%.2f€' % cont_ren_a

            if '_r2' in base:
                desc_rb += ']'

            desc_lb += '%.2f€ ' \
                       '- %.2f€' % (cont_lim_a, lim_rss_a)

        if '_r2' in base:
            desc_rb += ' × %.2f' % coef

        desc += desc_rb
        desc += desc_lb
        desc += desc_rbl
        return desc

    def calcul(cont_ren_a, cont_lim_a):

        if en_deduction:
            rb_a = cont_ren_a - ren_rss_a
            lb_a = cont_lim_a - lim_rss_a
        else:
            rb_a = cont_ren_a
            lb_a = cont_lim_a - lim_rss_a

        coef = 1
        if '_r2' in base:
            coef = switch_coef_r2(base, tip, tx_X)
            if coef is None:
                return

        rb_a *= coef
        rb_a = arrondir(rb_a, precision)
        rbl_a = arrondir(min(rb_a, lb_a), precision)

        description = description_rente_base(cont_ren_a=cont_ren_a,
                                             cont_lim_a=cont_lim_a, rb_a=rb_a,
                                             lb_a=lb_a, rbl_a=rbl_a, coef=coef)

        return rb_a, lb_a, rbl_a, description

    # Indemnité de base
    res_calcul = calcul(cont_ren_a=cont_ren_a, cont_lim_a=cont_lim_a)

    if res_calcul is None:
        return

    rb_a, lb_a, rbl_a, desc_ib = res_calcul
    if liste_rv_ren is not None and liste_rv_lim is not None:
        for i, rv in enumerate(liste_rv_ren):
            rv_lim = liste_rv_lim[i]
            # Revalo traitement
            cont_ren_a = rv['contractuel_a']
            cont_lim_a = rv_lim['contractuel_a']
            res_calcul_rv = calcul(cont_ren_a=cont_ren_a,
                                   cont_lim_a=cont_lim_a)
            if res_calcul_rv is None:
                return
            rb, lb, rbl, desc = res_calcul_rv
            rv['rente_base_a'] = rb
            rv['limite_base_a'] = lb
            rv['rente_base_limite_a'] = rbl
            rv['description_rente_base_limite_a'] = desc

    return rb_a, lb_a, rbl_a, desc_ib, liste_rv_ren


def cumul_deduction(ded_a, base_a):

    def description_cumul_deduction(presta_a):
        desc_presta_a = '\n'
        desc_presta_a += 'La rente annuelle avec déduction ' \
                         '(prestations annexes) est de %.2f€\n' \
                         % max(presta_a, 0)
        return desc_presta_a

    presta_a = min(ded_a, base_a)
    presta_a = max(0, presta_a)
    desc_presta_a = description_cumul_deduction(presta_a)

    return presta_a, desc_presta_a


# TODO vérifier revalo traitement
def rv_traitement(l_rv_rente, l_rv_deduction):

    # Indemnité de base
    if l_rv_rente is not None and l_rv_deduction is not None:
        for i, (rb, ded) in enumerate(zip(l_rv_rente, l_rv_deduction)):

            # RENTE DE BASE LIMITE
            rbl_a_i = rb['rente_base_limite_a']

            # DEDUCTION
            ded_a_i = ded['deduction_a']

            # PRESTA
            presta_a_i, desc_presta_a_i = cumul_deduction(
                ded_a=ded_a_i, base_a=rbl_a_i
            )

            rb['prestation_a'] = presta_a_i
            rb['description_prestation_a'] = desc_presta_a_i

    return l_rv_rente


def ri_salaire(debut, fin, duree_max, en_deduction, prime, ren_1, tx_ren_1,
               rss_ren_1, rass_1_b, rass_1_n, ren_2, tx_ren_2, rss_ren_2,
               rass_2_b, rass_2_n, ren_3, tx_ren_3, rss_ren_3, rass_3_b,
               rass_3_n, ren_at, tx_ren_at, rss_ren_at, rass_at_b, rass_at_n,
               lim_1, tx_lim_1, rss_lim_1, lim_2, tx_lim_2, rss_lim_2, lim_3,
               tx_lim_3, rss_lim_3, lim_at, tx_lim_at, rss_lim_at, deduction,
               tx_ded, rss_ded, mode_ded, prorata_1a, prorata_dc, cat, tip, ta,
               revalo_init, assiette, indice, nb_j, date_ref, freq, prem_rv,
               precision=0.01):

    dp, fp = debut, fin
    dat = date_debut_arret_de_travail()
    dpi = date_premiere_invalidite()

    ###############
    # DEBUT DEBUG #
    ###############

    desc_debug = '\nRI_SALAIRE_TRANCHE :\n'
    desc_debug += 'PERIODE : du %s au %s\n' % \
                  (formater_date(dp), formater_date(fp))
    desc_debug += '\nDurée max : %s\n' % duree_max

    lim_fp, desc_lim_periode, bloquant = gestion_duree_max(duree_max, dat, fp)
    fp_min = min(fp, lim_fp)
    if fp_min < fp:
        if bloquant:
            if dp > fp_min:
                # TODO TEST
                message_erreur = 'La date de début de la période %s ' \
                                 'est postérieure à la date de fin ' \
                                 'autorisée %s.\n' % \
                                 (dp, fp_min)
                ajouter_erreur(message_erreur)
                return

            # TODO TEST
            message_avertissement = 'La date de fin de la période %s ' \
                                    'a été réduite automatiquement ' \
                                    'à la date de fin autorisée %s.\n' % \
                                    (fp, fp_min)
            ajouter_avertissement(message_avertissement)
            fp = fp_min
            desc_debug += desc_lim_periode + ' : %s\n' % (formater_date(fp))
        else:
            # TODO TEST
            message_avertissement = 'Si nécessaire, ' \
                                    'la date de fin de la période %s ' \
                                    'doit être réduite manuellement ' \
                                    'à la date de fin conseillée %s.\n' % \
                                    (fp, fp_min)

            message_avertissement += desc_lim_periode
            ajouter_avertissement(message_avertissement)

    desc_debug += 'Deduction : %s\n' % (
        'oui' if en_deduction
        else 'non'
    )

    labels = ['r1',
              'r2',
              'r3',
              'rat']

    l_ren = [ren_1, ren_2, ren_3, ren_at]
    l_tx_ren = [tx_ren_1, tx_ren_2, tx_ren_3, tx_ren_at]
    l_rss_ren = [rss_ren_1, rss_ren_2, rss_ren_3, rss_ren_at]

    l_lim = [lim_1, lim_2, lim_3, lim_at]
    l_tx_lim = [tx_lim_1, tx_lim_2, tx_lim_3, tx_lim_at]
    l_rss_lim = [rss_ren_1, rss_ren_2, rss_ren_3, rss_ren_at]

    l_rss_brut = [rass_1_b, rass_2_b, rass_3_b, rass_at_b]
    l_rss_net = [rass_2_n, rass_2_n, rass_3_n, rass_at_n]

    tx_X = 0
    if tx_ren_1 is not None:
        tx_X = tx_ren_1[0]

    for (label, base_ren, tx_ren, lim, tx_lim,
         rss_ren, rss_lim, rjss_b, rjss_n) in \
            zip(labels, l_ren, l_tx_ren, l_lim, l_tx_lim,
                l_rss_ren, l_rss_lim, l_rss_brut, l_rss_net):

        if label in cat:

            desc_debug += '\nRente %s : %s\n' % (label, base_ren)
            desc_debug += 'Taux rente %s : %s\n' % (label, tx_ren)
            desc_debug += 'RSS %s rente : %s\n' % (label, rss_ren)

            desc_debug += '\nLimite %s : %s\n' % (label, lim)
            desc_debug += 'Taux limite %s : %s\n' % (label, tx_lim)
            desc_debug += 'RSS %s limite : %s\n' % (label, rss_lim)

            desc_debug += '\nRSS %s Brut : %s\n' % (label, rjss_b)
            desc_debug += 'RSS %s Net : %s\n' % (label, rjss_n)

    desc_debug += '\nDéduction : %s\n' % deduction
    desc_debug += 'Taux déduction : %s\n' % tx_ded
    desc_debug += 'RSS déduction : %s\n' % rss_ded
    desc_debug += 'Mode déduction : %s\n' % mode_ded

    desc_debug += '\nProrata 1er arrérage : %s\n' % prorata_1a
    desc_debug += 'Prorata décès : %s\n' % prorata_dc

    desc_debug += '\nRevalo init salaire : %s\n' % (
        'oui' if revalo_init
        else 'non'
    )

    desc_debug += '\nIndice : %s\n' % indice
    desc_debug += 'Assiette : %s\n' % assiette
    desc_debug += 'Fréquence : %s\n' % freq
    desc_debug += 'Date référence : %s\n' % date_ref
    desc_debug += 'Première revalo : %s\n' % (
        prem_rv if nb_j is None else ('+ '
                                      + str(nb_j)
                                      + ' jour(s)')
    )

    desc_debug += '\n'
    desc_debug += '#'*80
    message_debug(desc_debug)

    #############
    # FIN DEBUG #
    #############

    desc = '\n'

    ##############
    # DEBUT BASE #
    ##############

    base_ren, tx_ren, rss_ren, tx_lim, rss_lim, desc_base_taux = base_taux(
        cat=cat, ren_1=ren_1, ren_2=ren_2, ren_3=ren_3, ren_at=ren_at,
        tx_ren_1=tx_ren_1, tx_ren_2=tx_ren_2, tx_ren_3=tx_ren_3,
        tx_ren_at=tx_ren_at, rss_ren_1=rss_ren_1, rss_ren_2=rss_ren_2,
        rss_ren_3=rss_ren_3, rss_ren_at=rss_ren_at, tx_lim_1=tx_lim_1,
        tx_lim_2=tx_lim_2, tx_lim_3=tx_lim_3, tx_lim_at=tx_lim_at,
        rss_lim_1=rss_lim_1, rss_lim_2=rss_lim_2, rss_lim_3=rss_lim_3,
        rss_lim_at=rss_lim_at, tip=tip)

    desc += desc_base_taux
    base_ren_remp = base_ren
    tx_ren_remp = tx_ren
    rss_ren_remp = rss_ren
    cat_ = cat
    # TODO QUELLE UTILISATION de rss_ren et rss_ren_remp ?

    if '_r2' in base_ren_remp:
        cat_ = 'r2'
        base_ren_remp, tx_ren_remp, rss_ren_remp, _, _, desc_base_taux = \
            base_taux(
                cat=cat_, ren_1=ren_1, ren_2=ren_2,
                ren_3=ren_3, ren_at=ren_at,
                tx_ren_1=tx_ren_1, tx_ren_2=tx_ren_2,
                tx_ren_3=tx_ren_3, tx_ren_at=tx_ren_at,
                rss_ren_1=rss_ren_1, rss_ren_2=rss_ren_2,
                rss_ren_3=rss_ren_3, rss_ren_at=rss_ren_at,
                tx_lim_1=tx_lim_1, tx_lim_2=tx_lim_2,
                tx_lim_3=tx_lim_3, tx_lim_at=tx_lim_at,
                rss_lim_1=rss_lim_1, rss_lim_2=rss_lim_2,
                rss_lim_3=rss_lim_3, rss_lim_at=rss_lim_at,
                tip=tip
            )
        desc += 'SELON R2'
        desc += desc_base_taux

    ajouter_info(desc)

    # TRANCHES BASE
    res_tr_ren_sans_avec = tranches_sans_avec(base=base_ren_remp)

    if res_tr_ren_sans_avec is None:
        return

    tr_ren_sans, tr_ren_avec = res_tr_ren_sans_avec
    tr_ren, desc_tr_ren = tranches_lim_prime(prime, tr_ren_sans, tr_ren_avec)

    # TRANCHES LIMITE
    res_tr_lim_sans_avec = tranches_sans_avec(base=lim_1)

    if res_tr_lim_sans_avec is None:
        return

    tr_lim_sans, tr_lim_avec = res_tr_lim_sans_avec
    tr_lim, desc_tr_lim = tranches_lim_prime(prime, tr_lim_sans, tr_lim_avec)

    # TRANCHES DEDUCTION
    res_tr_ded_sans_avec = tranches_sans_avec(base=deduction)

    if res_tr_ded_sans_avec is None:
        return

    tr_ded_sans, tr_ded_avec = res_tr_ded_sans_avec
    tr_ded, desc_tr_ded = tranches_lim_prime(prime, tr_ded_sans, tr_ded_avec)

    # INDEX DERNIERE POSITION DE LISTE EN CAS DE REVALO INITIALE
    index_dpi = -1

    #############
    # REFERENCE #
    #############

    nbj_an_rente_trai = 365  # TMP

    # Periodes de revalorisations fournies : forcer les valeurs réelles des
    # indices
    ref_debut = dp
    ref_fin = fp
    ref_periodes = None
    ref_freq = freq

    if assiette == 'prestation' and revalo_init:

        # DEBUT CGT ASSUREUR
        res_sortie_contrat = rule_cgt_gestion_contrat()
        if res_sortie_contrat is None:
            return

        _, _, _, date_sortie, _ = res_sortie_contrat

        ref_debut = dpi
        ref_fin = dpi

        ref_periodes = [(ref_debut, ref_fin)]
        ref_freq = 'changement_taux'  # AUCUN IMPACT

    # TODO COMPARER A ET B
    # RENTE
    res_ref_ren = reference(tranches=tr_ren, pcts=tx_ren_remp, label='RENTE',
                            debut=ref_debut, fin=ref_fin, ind=indice,
                            freq=ref_freq, date_ref=date_ref, prem_rv=prem_rv,
                            nb_j=nb_j, nbj_par_an=nbj_an_rente_trai,
                            periodes=ref_periodes, base='annee',
                            type=base_ren_remp)

    if res_ref_ren is None:
        return

    _, ref_ren_a, desc_ref_ren, _, l_rv_ren = res_ref_ren

    # LIMITE
    res_ref_lim = reference(tranches=tr_lim, pcts=tx_lim, label='LIMITE',
                            debut=ref_debut, fin=ref_fin, ind=indice,
                            freq=ref_freq, date_ref=date_ref, prem_rv=prem_rv,
                            nb_j=nb_j, nbj_par_an=nbj_an_rente_trai,
                            periodes=ref_periodes, base='annee', type=lim_1)

    if res_ref_lim is None:
        return

    _, ref_lim_a, desc_ref_lim, _, l_rv_lim = res_ref_lim

    # DEDUCTION
    res_ref_ded = reference(
        tranches=tr_ded, pcts=tx_ded, label='DEDUCTION', debut=ref_debut,
        fin=ref_fin, ind=indice, freq=ref_freq, date_ref=date_ref,
        prem_rv=prem_rv, nb_j=nb_j, nbj_par_an=nbj_an_rente_trai,
        periodes=ref_periodes, base='annee', type=deduction
    )

    if res_ref_ded is None:
        return

    _, ref_ded_a, desc_ref_ded, _, l_rv_ded = res_ref_ded

    ###############
    # CONTRACTUEL #
    ###############

    ref_liste_ren_rv = None
    ref_liste_lim_rv = None
    ref_liste_ded_rv = None

    # Assiette traitement ou revalorisation initiale
    if not(assiette == 'prestation' and not revalo_init):
        ref_liste_ren_rv = l_rv_ren
        ref_liste_lim_rv = l_rv_lim
        ref_liste_ded_rv = l_rv_ded

    # RENTE
    _, cont_a, desc_cont_ren, l_rv_ren = contractuel(
        tranches=tr_ren, pcts=tx_ren_remp,
        nbj_par_an=nbj_an_rente_trai, label='RENTE',
        liste_rv=ref_liste_ren_rv, base='annee'
    )

    # LIMITE
    _, cont_lim_a, desc_cont_lim, l_rv_lim = contractuel(
        tranches=tr_lim, pcts=tx_lim,
        nbj_par_an=nbj_an_rente_trai, label='LIMITE',
        liste_rv=ref_liste_lim_rv, base='annee'
    )

    # DEDUCTION
    _, cont_ded_a, desc_cont_ded, l_rv_ded = contractuel(
        tranches=tr_ded, pcts=tx_ded,
        nbj_par_an=nbj_an_rente_trai, label='DEDUCTION',
        liste_rv=ref_liste_ded_rv, base='annee'
    )

    #######
    # RSS #
    #######

    # SELON CATEGORIE (R1,R2,R3,RAT,DEDUCTION) ET TYPE (BRUT/NET)
    # rss_base B/N OK
    # rss_lim B/N OK
    # rss_deduction B/N OK
    # lim deduction B/N
    # salaire maintenu B/N KO
    # pole emploi B/N OK
    # autre revenus OK

    # RENTE
    res_rss_ren = switch_rss_categorie_salaire(
        type_rss1=rss_ren_1, type_rss2=rss_ren_2, type_rss3=rss_ren_3,
        type_rssrat=rss_ren_at, rss1_n=rass_1_n, rss1_b=rass_1_b,
        rss2_n=rass_2_n, rss2_b=rass_2_b, rss3_n=rass_3_n, rss3_b=rass_3_b,
        rssat_n=rass_at_n, rssat_b=rass_at_b,
        cat=cat_ if cat == 'r1' else cat)

    if res_rss_ren is None:
        return

    type_rss_ren, ren_rss_a, desc_ren_rss_a = res_rss_ren

    # LIMITE
    res_rss_lim = switch_rss_categorie_salaire(
        type_rss1=rss_lim_1, type_rss2=rss_lim_2, type_rss3=rss_lim_3,
        type_rssrat=rss_lim_at, rss1_n=rass_1_n, rss1_b=rass_1_b,
        rss2_n=rass_2_n, rss2_b=rass_2_b, rss3_n=rass_3_n, rss3_b=rass_3_b,
        rssat_n=rass_at_n, rssat_b=rass_at_b, cat=cat)

    if res_rss_lim is None:
        return

    type_rss_lim, lim_rss_a, desc_lim_rss_a = res_rss_lim

    # DEDUCTION
    res_rss_ded = switch_rss_categorie_salaire(
        type_rss1=rss_ded, type_rss2=rss_ded, type_rss3=rss_ded,
        type_rssrat=rss_ded, rss1_n=rass_1_n, rss1_b=rass_1_b, rss2_n=rass_2_n,
        rss2_b=rass_2_b, rss3_n=rass_3_n, rss3_b=rass_3_b, rssat_n=rass_at_n,
        rssat_b=rass_at_b, cat=cat)

    if res_rss_ded is None:
        return

    type_rss_ded, ded_rss_a, desc_ded_rss_a = res_rss_ded

    ########################################################
    # RENTE DE BASE, LIMITE DE BASE, RENTE DE BASE LIMITEE #
    ########################################################

    res_rente_de_base = rente_de_base(cont_ren_a=cont_a, cont_lim_a=cont_lim_a,
                                      ren_rss_a=ren_rss_a, lim_rss_a=lim_rss_a,
                                      en_deduction=en_deduction, tx_X=tx_X,
                                      base=base_ren, tip=tip,
                                      liste_rv_ren=l_rv_ren,
                                      liste_rv_lim=l_rv_lim)

    if res_rente_de_base is None:
        return

    rente_a, lim_a, rente_lim_a, desc_rb, l_rv_ren = res_rente_de_base

    base_a = rente_lim_a
    reval_a = 0

    ded_a, desc_ded, rv_ded_liste = switch_mode_deduction(
        mode_ded=mode_ded, cont_ded_a=cont_ded_a, ded_rss_a=ded_rss_a, ta=ta,
        dp=dp, fp=fp, liste_rv_ded=l_rv_ded
    )

    # APPLIQUER LES TAUX DE DEVALORISATION
    ref_ren_a_rvi, ref_lim_a_rvi, ref_ded_a_rvi = -1, -1, -1
    cont_ren_a_rvi, cont_lim_a_rvi, cont_ded_a_rvi = -1, -1, -1
    ren_a_rvi, lim_a_rvi, ren_lim_a_rvi = -1, -1, -1
    ded_a_rvi = -1

    if assiette == 'prestation' and revalo_init:

        # REFERENCES
        ref_ren_a_rvi = l_rv_ren[index_dpi]['reference_a']
        desc_ref_ren = l_rv_ren[index_dpi]['description_reference']

        ref_lim_a_rvi = l_rv_lim[index_dpi]['reference_a']
        desc_ref_lim = l_rv_lim[index_dpi]['description_reference']

        ref_ded_a_rvi = l_rv_ded[index_dpi]['reference_a']

        # CONTRACTUELS
        cont_ren_a_rvi = l_rv_ren[index_dpi]['contractuel_a']
        desc_cont_ren = l_rv_ren[index_dpi]['description_contractuel']

        cont_lim_a_rvi = l_rv_lim[index_dpi]['contractuel_a']

        cont_ded_a_rvi = l_rv_ded[index_dpi]['contractuel_a']

        # RENTE LIMITE
        ren_a_rvi = l_rv_ren[index_dpi]['rente_base_a']
        lim_a_rvi = l_rv_ren[index_dpi]['limite_base_a']
        ren_lim_a_rvi = l_rv_ren[index_dpi]['rente_base_limite_a']
        desc_rb = l_rv_ren[index_dpi]['description_rente_base_limite_a']

        # DEVALORISATION
        res_rv = rule_revalorisation_privee(
            debut=ref_debut, fin=ref_fin, indice=indice,
            date_reference=date_ref, premiere_revalorisation=prem_rv,
            frequence=ref_freq, nombre_jours=nb_j,
            montant_journalier=ren_lim_a_rvi, inversion=True,
            periodes=ref_periodes
        )

        if isinstance(res_rv, dict) and 'erreur' in res_rv:
            ajouter_erreur(res_rv['erreur'])
            return

        l_rente_lim_rv, _ = res_rv

        base_a = l_rente_lim_rv[index_dpi]['base_amount']
        desc_base_a = l_rente_lim_rv[index_dpi]['description']

        reval_a = ren_lim_a_rvi - base_a

        # DEDUCTION
        ded_a_rvi = rv_ded_liste[index_dpi]['deduction_a']
        desc_ded = rv_ded_liste[index_dpi]['description_deduction_a']

    presta_a, desc_presta_a = cumul_deduction(
        ded_a_rvi if revalo_init and assiette == 'prestation' else ded_a,
        base_a
    )

    dec_360 = Decimal(360)
    presta_a = arrondir(presta_a, precision)
    presta_j = arrondir(presta_a / dec_360, precision)

    # Revalo post
    tmp_list = None
    if assiette == 'prestation':
        l_rv_ren = rv_prestation(
            debut=dp, fin=fp, indice=indice, freq=freq, date_ref=date_ref,
            prem_revalo=prem_rv, nb_j=nb_j, deduction=en_deduction,
            cont_j=0, iss_plein_j=0, ib_j=0, p_j=presta_a
        )

        tmp_list = len(l_rv_ren)*[{}]

    elif assiette == 'traitement':
        l_rv_ren = rv_traitement(
            l_rv_rente=l_rv_ren, l_rv_deduction=rv_ded_liste
        )

    else:
        message_erreur = 'Assiette de revalorisation invalide.'
        ajouter_erreur(message_erreur)
        return

    if l_rv_ren is None:
        return

    res = []
    num_sp = 1

    desc_taux = description_taux(base_ren, cat, cat_, tx_ren, tx_ren_remp)

    for j, (rv_ren, rv_lim, rv_ded) in enumerate(
            zip(l_rv_ren,
                l_rv_lim if assiette == 'traitement' else tmp_list,
                rv_ded_liste if assiette == 'traitement' else tmp_list)
    ):

            dsp_rv = rv_ren['start_date']
            fsp_rv = rv_ren['end_date']

            # PRESTATION
            if assiette == 'prestation':
                # TODO uniformiser avec production

                # DEBUT REVALORISATION #
                presta_a_i = rv_ren['prestation_revalorisee_j']

                # DEBUT DESCRIPTION #
                desc_rv_p = rv_ren['description_prestation_revalorisee']

            # TRAITEMENT
            elif assiette == 'traitement':

                # DEBUT REVALORISATION #
                presta_a_i = rv_ren['prestation_a']

                ref_ren_rv_a = rv_ren['reference_a']
                cont_ren_rv_a = rv_ren['contractuel_a']

                ref_lim_rv_a = rv_lim['reference_a']
                cont_lim_rv_a = rv_lim['contractuel_a']

                ref_ded_rv_a = rv_ded['reference_a']
                cont_ded_rv_a = rv_ded['contractuel_a']

                rb_a_i = rv_ren['rente_base_a']
                lb_a_i = rv_ren['limite_base_a']
                rbl_a_i = rv_ren['rente_base_limite_a']

                ded_a_i = rv_ded['deduction_a']

                # DEBUT DESCRIPTION #
                desc_ref_ren = rv_ren['description_reference']
                desc_cont_ren = rv_ren['description_contractuel']

                desc_ref_lim = rv_lim['description_reference']

                desc_ded = rv_ded['description_deduction_a']

                desc_rb = rv_ren['description_rente_base_limite_a']
                desc_presta_a = rv_ren['description_prestation_a']

            else:
                message = 'Assiette de revalorisation invalide %s' % assiette
                ajouter_erreur(message)
                return

            #####################
            # DEBUT DESCRIPTION #
            #####################

            desc_p_rv = ''

            # REFERENCE (REVALORISE TRAITEMENT OU INITIAL)
            desc_p_rv += 'SALAIRE DE REFERENCE ANNUEL\n'
            desc_p_rv += desc_ref_ren
            desc_p_rv += desc_ref_lim

            # TAUX
            desc_p_rv += '\nGARANTIE'
            desc_p_rv += desc_taux

            # CONTRACTUEL
            desc_p_rv += '\n\nSALAIRE CONTRACTUEL ANNUEL\n'
            desc_p_rv += desc_cont_ren

            # RSS
            desc_p_rv += '\nRENTE SECURITE SOCIALE ANNUELLE'
            desc_p_rv += desc_ren_rss_a
            desc_p_rv += desc_lim_rss_a

            # RENTE HORS DEDUCTION (RENTE, LIMITE, RENTE LIMITEE)
            desc_p_rv += desc_rb

            # DEVALORISATION (INITIAL)
            if assiette == 'prestation' and revalo_init:
                desc_p_rv += '\nRENTE NON REVALORISEE ANNUELLE'
                desc_p_rv += desc_base_a

            # DEDUCTION
            desc_p_rv += desc_ded

            # RENTE AVEC DEDUCTION
            desc_p_rv += '\n'
            desc_p_rv += desc_presta_a

            # REVALORISATION (PRESTATION)
            if assiette == 'prestation':
                desc_p_rv += desc_rv_p

            ###################
            # FIN DESCRIPTION #
            ###################

            # NE PAS ARRONDIR
            presta_j_i = arrondir(presta_a_i / dec_360, precision)
            for (dsp, fsp, periode_entiere, prorata, unit) in \
                    periode_de_rente(dsp_rv, fsp_rv):
                # trimestre ou mois (prorata nb mois parcourus entièrement)
                if periode_entiere:
                    nb_of_unit = prorata * Decimal(30)
                else:
                    nb_of_unit = prorata

                unit = 'day'

                p_j, p_j_i, desc_cgt = rule_cgt_partage_prestation(
                    debut_periode=dsp, base_courante=presta_j,
                    base_reva_courante=presta_j_i)

                presta_t = nb_of_unit * p_j_i
                presta_t = arrondir(presta_t, precision)

                desc_p_t = description_prestation_totale(
                    prestation_j=p_j_i, nb_jours_prestation=nb_of_unit,
                    prestation_t=presta_t, type='ri', prestation_a=presta_a_i
                )

                desc_p_t = '\nPRESTATION' + desc_p_t

                mess_debug = '%s %s %s %s\n' % (p_j_i, unit, prorata, presta_t)
                message_debug(mess_debug)

                s_num_sp = str(num_sp)

                desc_periode = desc_p_rv
                desc_periode += desc_cgt

                desc_periode += desc_p_t

                # CAS GENERAL
                test_p = {
                    # NON REVALO INIT
                    # base
                    'ref_a': ref_ren_a,
                    'cont_a': cont_a,
                    'rente_a': rente_a,
                    # lim
                    'ref_lim_a': ref_lim_a,
                    'cont_lim_a': cont_lim_a,
                    'lim_a': lim_a,
                    # ded
                    'ref_ded_a': ref_ded_a,
                    'cont_ded_a': cont_ded_a,
                    'ded_a': ded_a,
                    # pres
                    'rente_lim_a': rente_lim_a,
                    # REVALO INIT
                    # base
                    'ref_a_rvi': ref_ren_a_rvi,
                    'cont_a_rvi': cont_ren_a_rvi,
                    'rente_a_rvi': ren_a_rvi,
                    # lim
                    'ref_lim_a_rvi': ref_lim_a_rvi,
                    'cont_lim_a_rvi': cont_lim_a_rvi,
                    'lim_a_rvi': lim_a_rvi,
                    # ded
                    'ref_ded_a_rvi': ref_ded_a_rvi,
                    'cont_ded_a_rvi': cont_ded_a_rvi,
                    'ded_a_rvi': ded_a_rvi,
                    # pres
                    'rente_lim_a_rvi': ren_lim_a_rvi,
                    'base_a': base_a,
                    'reval_a': reval_a,
                    'presta_a': presta_a,
                    # REVALO TRAITEMENT
                    # base
                    'ref_rv_a_' + s_num_sp:
                        ref_ren_rv_a if assiette == 'traitement' else -1,
                    'cont_rv_a_' + s_num_sp:
                        cont_ren_rv_a if assiette == 'traitement' else -1,
                    'rente_a_' + s_num_sp:
                        rb_a_i if assiette == 'traitement' else -1,
                    # lim
                    'ref_lim_rv_a_' + s_num_sp:
                        ref_lim_rv_a if assiette == 'traitement' else -1,
                    'cont_lim_rv_a_' + s_num_sp:
                        cont_lim_rv_a if assiette == 'traitement' else -1,
                    'lim_a_' + s_num_sp:
                        lb_a_i if assiette == 'traitement' else -1,
                    # ded
                    'ref_ded_rv_a_' + s_num_sp:
                        ref_ded_rv_a if assiette == 'traitement' else -1,
                    'cont_ded_rv_a_' + s_num_sp:
                        cont_ded_rv_a if assiette == 'traitement' else -1,
                    'ded_a_' + s_num_sp:
                        ded_a_i if assiette == 'traitement' else -1,
                    # presta
                    'rente_lim_a_' + s_num_sp:
                        rbl_a_i if assiette == 'traitement' else -1,
                    'presta_a_' + s_num_sp:
                        presta_a_i if assiette == 'traitement' else -1,
                    # REVALO PRESTA
                    'presta_a_rv_' + s_num_sp:
                        presta_a_i if assiette == 'prestation' else -1,
                    'presta_t_rv_' + s_num_sp:
                        presta_t if assiette == 'prestation' else -1,
                }

                res_p = {
                    'start_date': dsp,
                    'end_date': fsp,
                    'nb_of_unit': nb_of_unit,
                    'unit': unit,
                    'amount': max(presta_t, 0),
                    'base_amount': max(p_j, 0),
                    'amount_per_unit': max(p_j_i, 0),
                    'description': desc_periode,
                    'limit_date': None,
                    'extra_details': {
                        'tranche_a': str(tr_ren[0]),
                        'tranche_b': str(tr_ren[1]),
                        'tranche_c': str(tr_ren[2]),
                        'rass1_brut': str(rass_1_b),
                        'rass2_brut': str(rass_2_b),
                        'rass3_brut': str(rass_3_b),
                        'rassat_brut': str(rass_at_b),
                        'rass1_net': str(rass_1_n),
                        'rass2_net': str(rass_2_n),
                        'rass3_net': str(rass_3_n),
                        'rassat_net': str(rass_at_n),
                        'description_prev': desc_periode
                    },
                    'test_data': test_p
                }

                res.append(res_p)
                num_sp += 1

    return res


def rule_ri_salaire_tranche(
        duree, en_complement, prime,
        prorata_1a, prorata_dc,
        rss_rente, rss_limite,
        base_r1, base_r2, base_r3, base_rat, limite,
        mode_deduction,
        assiette, indice, frequence, prem_revalo, nbj_rv, date_ref,
        revalo_init,
        cat, rass1_b, rass1_n, rass2_b, rass2_n, rass3_b, rass3_n, raatss_b,
        raatss_n, tip, pcts_r1, pcts_r2, pcts_r3, pcts_rat, pcts_lim):
    '''
    :données complémentaires
        - rjss
        - rjss_corrigee
    :return:
    :rtype: list[dict[str, any]]
    '''

    ############
    # CONTEXTE #
    ############

    # PERIODE (debut, fin)
    dp = date_debut_periode_indemnisation()
    fp = date_fin_periode_indemnisation()

    # SALAIRES (brut, net)
    brut = salaire_brut()
    net = salaire_net()

    if brut is None:
        message_none = 'Salaire brut non renseigné.'
        ajouter_erreur(message_none)
        return
    elif brut <= 0:
        message = 'Salaire brut négatif ou nul.'
        ajouter_avertissement(message)

    ##############
    # PARAMETRES #
    ##############

    # GENERAL (deduction)
    en_deduction = not en_complement

    # RENTE INVALIDITE

    # TAUX de R1, R2, R3, RAT, et LIMITE
    label_pcts_r1 = 'Taux de catégorie R1'
    label_pcts_r2 = 'Taux de catégorie R2'
    label_pcts_r3 = 'Taux de catégorie R3'
    label_pcts_rat = 'Taux de catégorie RAT'
    label_pcts_lim = 'Taux de limite.'

    if 'r2' in base_r1 and '/' not in pcts_r1:
        pcts_r1 = str(pcts_r1) + '/0/0'

    if ('r2' in base_rat or 'corr' in base_rat) and '/' not in pcts_rat:
        pcts_rat = '0/0/0'

    pcts_r1 = chaine_vers_taux(pcts_r1, label_pcts_r1)
    pcts_r2 = chaine_vers_taux(pcts_r2, label_pcts_r2)
    pcts_r3 = chaine_vers_taux(pcts_r3, label_pcts_r3)
    pcts_rat = chaine_vers_taux(pcts_rat, label_pcts_rat)
    pcts_lim = chaine_vers_taux(pcts_lim, label_pcts_lim)

    for pcts in [pcts_r1, pcts_r2, pcts_r3, pcts_rat, pcts_lim]:
        if pcts is None:
            return

    # TESTS
    l_base_label = [
        (base_r1, 'Base r1'),
        (base_r2, 'Base r2'),
        (base_r3, 'Base r3'),
        (base_rat, 'Base rat'),
        (limite, 'Limite')
    ]

    for (base, label) in l_base_label:
        if base == 'net' and (net is None or (net is not None and net == 0)):
            message_net = 'Net non renseigné ' \
                          'pour le calcul en %s.' % label
            ajouter_erreur(message_net)
            return

    ###########
    # DONNEES #
    ###########

    # PRESTA
    ta = compl_taux_d_activite_mi_temps_therapeuthique()

    if mode_deduction == 'taux':
        if ta is None:
            message_none = "Taux d'activité non saisi."
            ajouter_erreur(message_none)
            return
        else:
            if ta < 0 or ta > 100:
                message_erreur = "Taux d'activité invalide."
                ajouter_erreur(message_erreur)
                return

    return ri_salaire(debut=dp, fin=fp, duree_max=duree,
                      en_deduction=en_deduction, prime=prime, ren_1=base_r1,
                      tx_ren_1=pcts_r1, rss_ren_1=rss_rente, rass_1_b=rass1_b,
                      rass_1_n=rass1_n, ren_2=base_r2, tx_ren_2=pcts_r2,
                      rss_ren_2=rss_rente, rass_2_b=rass2_b, rass_2_n=rass2_n,
                      ren_3=base_r3, tx_ren_3=pcts_r3, rss_ren_3=rss_rente,
                      rass_3_b=rass3_b, rass_3_n=rass3_n, ren_at=base_rat,
                      tx_ren_at=pcts_rat, rss_ren_at=rss_rente,
                      rass_at_b=raatss_b, rass_at_n=raatss_n, lim_1=limite,
                      tx_lim_1=pcts_lim, rss_lim_1=rss_limite, lim_2=limite,
                      tx_lim_2=pcts_lim, rss_lim_2=rss_limite, lim_3=limite,
                      tx_lim_3=pcts_lim, rss_lim_3=rss_limite, lim_at=limite,
                      tx_lim_at=pcts_lim, rss_lim_at=rss_limite,
                      deduction=limite, tx_ded=pcts_lim, rss_ded=rss_limite,
                      mode_ded=mode_deduction, prorata_1a=prorata_1a,
                      prorata_dc=prorata_dc, cat=cat, tip=tip, ta=ta,
                      revalo_init=revalo_init, assiette=assiette,
                      indice=indice, nb_j=nbj_rv, date_ref=date_ref,
                      freq=frequence, prem_rv=prem_revalo)


##########################
# DEBUT PARTIE GENERIQUE #
##########################

#####################
# DEBUT RI MANUELLE #
#####################


def donnees_rente():  # RI MANUELLE
    '''
    :données complémentaires:
        - rjss
        - ri_corrigee
        - description_ri_de_base_corrige
    :return:
    :rtype: list[dict[str,any]]
    '''

    ###########
    # DONNEES #
    ###########

    # EVENEMENT
    cat = compl_categorie_de_rente_d_invalidite()
    rass_b = compl_rass_brut()
    rass_n = compl_rass_net()
    tip = compl_taux_incapacite_permanente()

    # TESTS
    if cat is None:
        message_none = 'Catégorie de rente non saisie.'
        ajouter_erreur(message_none)
        return

    if rass_b is None:
        message_none = 'RSS brute non saisie.'
        ajouter_erreur(message_none)
        return

    if rass_n is None:
        message_none = 'RSS nette non saisie.'
        ajouter_erreur(message_none)
        return

    rass1_b, rass1_n = None, None
    rass2_b, rass2_n = None, None
    rass3_b, rass3_n = None, None
    rassat_b, rassat_n = None, None

    cinq = Decimal(5)
    trois = Decimal(3)

    if cat == 'r1':
        coef = cinq / trois
        rass1_b, rass1_n = rass_b, rass_n
        rass2_b, rass2_n = rass_b * coef, rass_n * coef
        rass3_b, rass3_n = rass2_b, rass2_n
    elif cat == 'r2':
        rass2_b, rass2_n = rass_b, rass_n
    elif cat == 'r3':
        rass3_b, rass3_n = rass_b, rass_n
    elif cat == 'rat':
        rassat_b, rassat_n = rass_b, rass_n

    categories = {
        'r1': (rass1_b, rass1_n, '1'),
        'r2': (rass2_b, rass2_n, '2'),
        'r3': (rass3_b, rass3_n, '3'),
        'rat': (rassat_b, rassat_n, 'AT'),
    }

    res = categories.get(cat, 'Catégorie de rente invalide %s' % cat)
    if isinstance(res, str):
        ajouter_erreur(res)
        return

    rass_b, rass_n, label = res
    res = rass_b is None and rass_n is None
    if res:
        message = 'RSS de catégorie %s non renseignées.' % label
        ajouter_erreur(message)
        return

    if cat == 'rat':
        if tip is None:
            message = "Taux d'incapacité permanente non renseigné."
            ajouter_erreur(message)
            return

    return cat, \
           rass1_b, rass1_n, \
           rass2_b, rass2_n, \
           rass3_b, rass3_n, \
           rassat_b, rassat_n, tip, \
           rass_b, rass_n


###################
# FIN RI MANUELLE #
###################


def blocage_non_implementee():

    cat = compl_categorie_de_rente_d_invalidite().lower()

    cat_r1 = cat == 'r1'
    base_r1 = param_03a_base_r1()

    cat_r2 = cat == 'r2'
    base_r2 = param_03b_base_r2()

    cat_r3 = cat == 'r3'
    base_r3 = param_03c_base_r3()

    cat_rat = cat == 'rat'
    base_rat = param_03d_base_rat()

    for base_i, cat_i in \
            [(base_r1, cat_r1),
             (base_r2, cat_r2),
             (base_r3, cat_r3),
             (base_rat, cat_rat)]:

        if cat_i and \
                (base_i in ['pss',
                            'psi',
                            'corr_r1r2_rat',
                            'corr_rente_rat',
                            '3tip/2_%_brut']
                 or 'raeg' in base_i):

            message_erreur = 'Les bases PSS, PSI, RAEG, ' \
                             'corr_r1r2_rat, corr_rente_rat, ' \
                             '3tip/2_%_brut ' \
                             'ne sont pas encore disponibles ' \
                             'en calcul automatique.'

            ajouter_erreur(message_erreur)
            return True

    return False


#####################
# DEBUT RI MANUELLE #
#####################

def sorties_rss_corrigee_ou_nulle(rass_b, rass_n, precision=0.01):

    ############
    # CONTEXTE #
    ############
    dp = date_debut_periode_indemnisation()
    fp = date_fin_periode_indemnisation()
    nbj_p = (fp - dp).days + 1

    # STRUCTURE RESULTAT
    test_p = {
        'reference_j': 0,
        'contractuel_j': 0,
        'rente_j': 0,
        'prestation_j': 0,
        'prestation_rv_j': 0,
    }

    description = ''
    res_p = {
        'start_date': dp,
        'end_date': fp,
        'nb_of_unit': nbj_p,
        'unit':
            'day',
        'amount': Decimal(0),
        'base_amount': Decimal(0),
        'amount_per_unit': Decimal(0),
        'description': description,
        'extra_details': {
            'rass_brut': str(rass_b),
            'rass_net': str(rass_n),
        },
        'test_data': test_p
    }

    res = [res_p]

    ri_base_corrigee_p = compl_ri_corrigee()
    ri_revalo_corrigee_p = compl_ri_revalo_corrigee()
    desc_ri_corrigee_p = compl_description_ri_de_base_corrige()

    # SORTIE RI CORRIGEE
    if (ri_base_corrigee_p is None) != (ri_revalo_corrigee_p is None):
        message_erreur = "Un montant de prestation corrigée n'est pas saisi."
        test_p['erreur'] = (-1, message_erreur)
        ajouter_erreur(message_erreur)
        return res

    if ri_base_corrigee_p is not None and ri_revalo_corrigee_p is not None:

        if ri_base_corrigee_p >= 0 and ri_revalo_corrigee_p >= 0:
            base_p = ri_base_corrigee_p
            revalo_p = ri_revalo_corrigee_p

            if revalo_p >= base_p and not (base_p == revalo_p == 0):
                message_erreur = 'La revalorisation corrigée est supérieure' \
                                 ' à la base corrigée.'
                test_p['erreur'] = (-3, message_erreur)
                ajouter_avertissement(message_erreur)

            presta_p = arrondir(
                ri_base_corrigee_p + ri_revalo_corrigee_p, precision
            )

            if desc_ri_corrigee_p is not None:
                description += desc_ri_corrigee_p + '\n'

            description += '\nPRESTATION\n'
            description += 'Base (période) : %.2f€' % base_p
            description += '\nRevalorisation (période) : %.2f€' % revalo_p
            description += '\nPrestation (période) : %.2f€' % presta_p

            res_p['amount'] = presta_p
            res_p['base_amount'] = arrondir(base_p / Decimal(nbj_p), precision)
            res_p['amount_per_unit'] = arrondir(presta_p / Decimal(nbj_p), precision)
            res_p['description'] = description

            test_p['prestation_j'] = \
                res_p['base_amount']
            test_p['prestation_rv_j'] = \
                res_p['amount_per_unit']
            message_debug(description)
            return res
        else:
            message_erreur = 'Un montant de prestation corrigée est négatif.'
            test_p['erreur'] = (-2, message_erreur)
            ajouter_erreur(message_erreur)
            return res

    # SORTIE RJSS NULLE
    if rass_b is not None and rass_b <= 0 \
            and rass_n is not None and rass_n <= 0:
        description = 'Aucune prestation à verser car la RSS est nulle.\n'
        res_p['description'] = description
        message_debug(description)
        return res

    # SORTIE AUCUNE REPRISE / MAINTIEN
    res_sortie_contrat = rule_cgt_gestion_contrat()
    if res_sortie_contrat is None:
        return

    regle_entree, regle_sortie, date_entree, date_sortie, exception = res_sortie_contrat
    if (regle_entree and regle_entree == 'normal_indemnifications'):
        message_erreur = 'Aucune reprise.'
        test_p['erreur'] = (-5, message_erreur)
        description = 'Aucune prestation à verser car aucune reprise de prestation à partir du %s.' % formater_date(date_entree)
        res_p['description'] = description
        return res

    if (regle_sortie and date_sortie and regle_sortie == 'stop_indemnifications' and dp > date_sortie):
        message_erreur = 'Aucun maintien.'
        test_p['erreur'] = (-6, message_erreur)
        description = 'Aucune prestation à verser car aucun maintien de prestation après le %s.' % formater_date(date_sortie)
        res_p['description'] = description
        return res

    return None

###################
# FIN RI MANUELLE #
###################


def parametres_rente():
    res_erreur = [
        {'test_data': {'erreur': (-99, 'parametre')}}
    ]

    ##############
    # PARAMETRES #
    ##############

    # GENERAL
    duree = param_01a_duree_presta()
    en_complement = param_01b_en_complement()
    prime = param_01c_prime()

    # TESTS
    if duree is None:
        message_none = 'Durée de prestation non renseignée.'
        ajouter_erreur(message_none)
        return False, res_erreur

    if en_complement is None:
        message_none = 'Calcul en déduction/complément non renseigné.'
        ajouter_erreur(message_none)
        return False, res_erreur

    if prime is None:
        message_none = 'Prime de référence non renseignée'
        ajouter_erreur(message_none)
        return False, res_erreur

    # PRORATA
    prorata_1a = param_02a_prorata_1a()
    prorata_dc = param_02b_prorata_dc()

    # TESTS
    if prorata_1a is None:
        message_none = 'Prorata premier arrerage non renseigné'
        ajouter_erreur(message_none)
        return False, res_erreur

    if prorata_dc is None:
        message_none = 'Prorata décès arrerage non renseigné'
        ajouter_erreur(message_none)
        return False, res_erreur

    # RSS
    rss_rente = param_03a1_rss_rente_base()
    rss_limite = param_03a2_rss_limite_base()

    if rss_rente is None:
        message = 'Type de rss de base non renseigné.'
        ajouter_avertissement(message)

    if rss_limite is None:
        message = 'Type de rss de limite non renseigné.'
        ajouter_avertissement(message)

    # BASES
    base_r1 = param_03a_base_r1()
    base_r2 = param_03b_base_r2()
    base_r3 = param_03c_base_r3()
    base_rat = param_03d_base_rat()
    limite = param_03e_limite()

    # TESTS
    l_base_label = [
        (base_r1, 'Base r1'),
        (base_r2, 'Base r2'),
        (base_r3, 'Base r3'),
        (base_rat, 'Base rat'),
        (limite, 'Limite')
    ]

    # TODO VERIFIER EN BDD
    for (base, label) in l_base_label:
        if base is None:
            message_none = '%s non renseignée.' % label
            ajouter_erreur(message_none)
            return False, res_erreur

    # DEDUCTIONS
    mode_deduction = param_03e_mode_deduction()

    # TESTS
    if mode_deduction is None:
        message_none = 'Mode de déduction non renseigné'
        ajouter_erreur(message_none)
        return False, res_erreur

    # REVALO
    # TODO UNIFORMISER param_05b,c avec l'ij
    assiette = param_05a_assiette_rv()
    indice = param_05b_indice_rv()
    frequence = param_05c_freq_rv()
    prem_revalo = param_05d_premiere_rv()
    nbj_rv = param_05e_nbj_rv()
    date_ref = param_05f_date_ref_rv()
    revalo_init = param_06a_revalo_init()

    # TESTS
    if assiette is None:
        message_none = 'Assiette revalorisation non renseignée'
        ajouter_erreur(message_none)
        return False, res_erreur

    if frequence is None:
        message_none = 'Frequence revalorisation non renseignée'
        ajouter_erreur(message_none)
        return False, res_erreur

    if indice is None:
        message_none = 'Indice de revalorisation non renseigné'
        ajouter_erreur(message_none)
        return False, res_erreur

    if prem_revalo is None:
        message_none = 'Première revalorisation non renseignée'
        ajouter_erreur(message_none)
        return False, res_erreur

    if date_ref is None:
        message_none = 'Date de référence revalorisation non renseignée'
        ajouter_erreur(message_none)
        return False, res_erreur

    if nbj_rv is None:
        if prem_revalo == 'nb_jour':
            message_none = 'Nombre de jours non renseigné'
            ajouter_erreur(message_none)
            return False, res_erreur
        else:
            nbj_rv = 0

    if revalo_init is None:
        message_none = 'Revalo initiale non renseignée.'
        ajouter_erreur(message_none)
        return False, res_erreur

    return True, (duree, en_complement, prime, \
           prorata_1a, prorata_dc, \
           rss_rente, rss_limite, \
           base_r1, base_r2, base_r3, base_rat, limite, \
           mode_deduction, \
           assiette, indice, frequence, prem_revalo, nbj_rv, date_ref, \
           revalo_init)

########################
# FIN PARTIE GENERIQUE #
########################


#####################
# DEBUT RI STANDARD #
#####################


def ri_classique():

    def specificites():

        # GESTION
        pcts_z = '0/0/0'

        pcts_r1 = param_03a_pcts_r1() if compl_0a_gestion_r1() else pcts_z
        pcts_r2 = param_03b_pcts_r2() if compl_0b_gestion_r2() else pcts_z
        pcts_r3 = param_03c_pcts_r3() if compl_0c_gestion_r3() else pcts_z
        pcts_rat = param_03d_pcts_rat() if compl_0d_gestion_rat() else pcts_z

        pcts_lim = param_03e_pcts_limite()

        return pcts_r1, pcts_r2, pcts_r3, pcts_rat, pcts_lim

    # DONNEES
    res = donnees_rente()
    if res is None:
        return

    cat, \
    rass1_b, rass1_n, \
    rass2_b, rass2_n, \
    rass3_b, rass3_n, \
    raatss_b, raatss_n, tip, \
    rass_b, rass_n = res

    # GENERAL

    # SORTIES PRIORITAIRES
    res_rss_corrigee_ou_nulle = sorties_rss_corrigee_ou_nulle(rass_b, rass_n)
    if res_rss_corrigee_ou_nulle is not None:
        return res_rss_corrigee_ou_nulle

    # PARAMETRE
    test, res = parametres_rente()
    if not test:
        return res

    duree, en_complement, prime, \
    prorata_1a, prorata_dc, \
    rss_rente, rss_limite, \
    base_r1, base_r2, base_r3, base_rat, limite, \
    mode_deduction, \
    assiette, indice, frequence, prem_revalo, nbj_rv, date_ref, \
    revalo_init = res

    # DONNEE
    res = specificites()
    if res is None:
        return
    pcts_r1, pcts_r2, pcts_r3, pcts_rat, pcts_lim = res

    # BLOCAGE
    if blocage_non_implementee():
        return

    return rule_ri_salaire_tranche(
        duree=duree, en_complement=en_complement, prime=prime,
        prorata_1a=prorata_1a, prorata_dc=prorata_dc,
        rss_rente=rss_rente, rss_limite=rss_limite,
        base_r1=base_r1, base_r2=base_r2, base_r3=base_r3, base_rat=base_rat,
        limite=limite,
        mode_deduction=mode_deduction,
        assiette=assiette, indice=indice, frequence=frequence,
        prem_revalo=prem_revalo, nbj_rv=nbj_rv, date_ref=date_ref,
        revalo_init=revalo_init,
        cat=cat, rass1_b=rass1_b, rass1_n=rass1_n, rass2_b=rass2_b,
        rass2_n=rass2_n, rass3_b=rass3_b, rass3_n=rass3_n, raatss_b=raatss_b,
        raatss_n=raatss_n, tip=tip, pcts_r1=pcts_r1, pcts_r2=pcts_r2,
        pcts_r3=pcts_r3, pcts_rat=pcts_rat, pcts_lim=pcts_lim
    )

return ri_classique() # DECOMMENTER SOUS COOG

###################
# FIN RI STANDARD #
###################
