# ---
# Name: Indemnité Journalière selon 1 palier (nouveau)
# Short Name: ij_salaire_tranche_1_palier_2018
# Type: benefit
# ---

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

###################
# DEBUT RI ENFANT #
###################

#####################
# DEBUT RI STANDARD #
#####################

#####################
# DEBUT IJ STANDARD #
#####################

# Méthodes d'aide au calcul
caractere_separateur_tranches = '/'
caractere_separateur_classes = '$'
caractere_separateur_inf_sup = ':'


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


##########################
# FIN IJ PALIER STANDARD #
# DEBUT IJ PALIER STANDARD #
############################

###################
# DEBUT IJ PALIER #
###################


def ij_un_palier(specificites):

    # GENERAL

    # SORTIES PRIORITAIRES
    res_sorties_ijss_corrigee_ou_nulle = \
        rule_sorties_ijss_corrigee_ou_nulle(precision=None)
    message_erreur = recuperer_erreur(res_sorties_ijss_corrigee_ou_nulle)

    if message_erreur:
        return {'erreur': message_erreur}
    if res_sorties_ijss_corrigee_ou_nulle is not None:
        return res_sorties_ijss_corrigee_ou_nulle

    # PARAMETRE
    res = rule_ij_parametres_generiques(
        a01a_duree_presta=param_a01a_duree_presta(),
        a01c_prime=param_a01c_prime(),
        a02c_lim_av_rup=param_a02c_lim_av_rup(),
        a02d_pcts_lim_av_rup=param_a02d_pcts_lim_av_rup(),
        a02e_rv_lim_av_rup=param_a02e_rv_lim_av_rup(),
        a03c_lim_ap_rup=param_a03c_lim_ap_rup(),
        a03d_pcts_lim_ap_rup=param_a03d_pcts_lim_ap_rup(),
        a03e_rv_lim_ap_rup=param_a03e_rv_lim_ap_rup(),
        a04a_red_ib_mt=param_a04a_red_ib_mt(),
        a04b_lim_mt=param_a04b_lim_mt(),
        a04c_rv_lim_mt=param_a04c_rv_lim_mt(),
        a05a_assiette_rv=param_a05a_assiette_rv(),
        a05b_freq_rv=param_a05b_freq_rv(),
        a05c_indice_rv=param_a05c_indice_rv(),
        a05d_premiere_rv=param_a05d_premiere_rv(),
        a05e_date_ref_rv=param_a05e_date_ref_rv(),
        a05f_nbj_rv=param_a05f_nbj_rv(),
        a07_convertir_ijss_brut_vers_net=\
            param_a07_convertir_ijss_brut_vers_net()
    )
    message_erreur = recuperer_erreur(res)

    if message_erreur:
        return {'erreur': message_erreur}

    duree, prime, \
    lim_av_rup, pcts_lim_av_rup, rv_lim_av_rup, \
    lim_ap_rup, pcts_lim_ap_rup, rv_lim_ap_rup, \
    red_ib_mt, lim_mt, rv_lim_mt, \
    assiette, freq, indice, premiere, date_ref, nbj_rv, \
    convertir_ijss_brut_vers_net = res

    # DONNEE
    res = specificites()
    if res is None:
        return
    complement = res[0]
    reference_palier = res[1]
    if reference_palier == 'dat':
        depart = date_debut_arret_de_travail()
    elif reference_palier == 'dei':
        depart = ajouter_jours(date_fin_franchise(), 1)
    else:
        message = 'Date de référence de palier invalide %s.' % \
                  reference_palier
        return {'erreur': message}

    duree_0 = res[2]
    fp_0_incluse = ajouter_jours(depart, duree_0)
    dp, fp = date_debut_periode_indemnisation(), date_fin_periode_indemnisation()
    message_avertissement = None
    message_erreur = None
    if fp_0_incluse < dp: # appliquer palier 2
        debuts = [dp]
        fins = [fp]
        i = 1
        l_bases_av_rup = [res[3][i]]
        l_pcts_base_av_rup = [res[4][i]]
        l_bases_ap_rup = [res[5][i]]
        l_pcts_base_ap_rup = [res[6][i]]
        message_avertissement = 'Un changement de palier intervient ' \
                                'avant la période le %s.\n' % \
                                formater_date(fp_0_incluse)
        message_avertissement += 'Application du palier 2 uniquement.'
    elif fp > fp_0_incluse >= dp:
        debuts = [dp, ajouter_jours(fp_0_incluse, 1)]
        fins = [fp_0_incluse, fp]
        l_bases_av_rup = res[3]
        l_pcts_base_av_rup = res[4]
        l_bases_ap_rup = res[5]
        l_pcts_base_ap_rup = res[6]
        message_avertissement = 'Un changement de palier intervient ' \
                                'pendant la période le %s.\n' % \
                                formater_date(fp_0_incluse)
    elif fp_0_incluse >= fp:  # appliquer palier 1
        debuts = [dp]
        fins = [fp]
        i = 0
        l_bases_av_rup = [res[3][i]]
        l_pcts_base_av_rup = [res[4][i]]
        l_bases_ap_rup = [res[5][i]]
        l_pcts_base_ap_rup = [res[6][i]]
        message_avertissement = 'Un changement de palier intervient ' \
                                'après la période le %s.\n' % \
                                formater_date(fp_0_incluse)
        message_avertissement += 'Application du palier 1 uniquement.'
    else:
        message_erreur = 'Cas incorrect des paliers : ' \
                         '%s (debut) %s (fin) %s (palier) ' % \
                         (formater_date(dp),
                          formater_date(fp),
                          formater_date(fp_0_incluse))

    if message_avertissement is not None:
        avertir(message_avertissement)

    if message_erreur is not None:
        return {'erreur': message_erreur}

    # TODO: déplacer dans les paramètres génériques
    type_deduction_recccn = param_a06a_type_deduction_recccn()

    res = []
    for (debut, fin, base_av_rup, pcts_base_av_rup, base_ap_rup, pcts_base_ap_rup) in \
            zip(debuts, fins, l_bases_av_rup, l_pcts_base_av_rup, l_bases_ap_rup, l_pcts_base_ap_rup):

        res_palier = rule_ij_salaire_standard(
            duree=duree, en_complement=complement, prime=prime,
            base_av_rup=base_av_rup, pcts_base_av_rup=pcts_base_av_rup,
            lim_av_rup=lim_av_rup, pcts_lim_av_rup=pcts_lim_av_rup,
            rv_lim_av_rup=rv_lim_av_rup, base_ap_rup=base_ap_rup,
            pcts_base_ap_rup=pcts_base_ap_rup, lim_ap_rup=lim_ap_rup,
            pcts_lim_ap_rup=pcts_lim_ap_rup, rv_lim_ap_rup=rv_lim_ap_rup,
            red_ib_mt=red_ib_mt, lim_mt=lim_mt, rv_lim_mt=rv_lim_mt,
            assiette_rv=assiette, freq_rv=freq, indice_rv=indice,
            premiere_rv=premiere, date_ref_rv=date_ref, nbj_rv=nbj_rv,
            convertir_ijss_brut_vers_net=convertir_ijss_brut_vers_net,
            type_deduction_recccn=type_deduction_recccn, debut=debut, fin=fin
        )
        message_erreur = recuperer_erreur(res_palier)
        if message_erreur:
            return {'erreur': message_erreur}
        res.extend(res_palier)
        si_avertissement_lever_avertissement(res_palier)

    return res

#################
# FIN IJ PALIER #
#################

#########################
# FIN IJ PALIER X MOTIF #
#########################

def ij_un_palier_standard():

    def specificites_palier_standard():
        # Paramètres
        complement = param_a01b_en_complement()  # TODO déplacer en spécifique
        reference_palier = param_a02b_date_ref_palier()
        duree_0 = max(0, param_a02b_duree_palier_0() - 1)

        base_av_rup_0 = param_a02a_base_av_rup_0()
        pcts_base_av_rup_0 = param_a02b_pcts_base_av_rup_0()

        base_av_rup_1 = param_a02b_base_av_rup_1()
        pcts_base_av_rup_1 = param_a02b_pcts_base_av_rup_1()

        base_ap_rup_0 = param_a03a_base_ap_rup_0()
        pcts_base_ap_rup_0 = param_a03b_pcts_base_ap_rup_0()

        base_ap_rup_1 = param_a03b_base_ap_rup_1()
        pcts_base_ap_rup_1 = param_a03b_pcts_base_ap_rup_1()

        return [complement, reference_palier, duree_0, [base_av_rup_0, base_av_rup_1], [pcts_base_av_rup_0, pcts_base_av_rup_1], [base_ap_rup_0, base_ap_rup_1], [pcts_base_ap_rup_0, pcts_base_ap_rup_1]]

    resultats = ij_un_palier(specificites_palier_standard)
    si_erreur_lever_erreur(resultats)

    return resultats

return ij_un_palier_standard() # DECOMMENTER SOUS COOG

##########################
# FIN IJ PALIER STANDARD #
