# ---
# Name: Indemnité Journalière classique (nouveau)
# Short Name: ij_salaire_tranche_2018
# Type: benefit
# ---

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
# DEBUT IJ CLASSIQUE #
######################


def ij_classique():

    def specificites():
        # GESTION
        complement = param_a01b_en_complement()

        base_av_rup = param_a02a_base_av_rup()
        pcts_base_av_rup = param_a02b_pcts_base_av_rup()

        base_ap_rup = param_a03a_base_ap_rup()
        pcts_base_ap_rup = param_a03b_pcts_base_ap_rup()

        # TODO: déplacer dans les paramètres génériques
        type_deduction_recccn = param_a06a_type_deduction_recccn()

        return complement, base_av_rup, pcts_base_av_rup, base_ap_rup, \
            pcts_base_ap_rup, type_deduction_recccn

    # GENERAL

    # SORTIES PRIORITAIRES
    res_sorties_ijss_corrigee_ou_nulle = \
        rule_sorties_ijss_corrigee_ou_nulle(precision=None)
    si_erreur_lever_erreur(res_sorties_ijss_corrigee_ou_nulle)
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
            param_a07_convertir_ijss_brut_vers_net())
    if si_erreur_lever_erreur(res):
        return

    duree, prime, \
    lim_av_rup, pcts_lim_av_rup, rv_lim_av_rup, \
    lim_ap_rup, pcts_lim_ap_rup, rv_lim_ap_rup, \
    red_ib_mt, lim_mt, rv_lim_mt, \
    assiette, freq, indice, premiere, date_ref, nbj_rv, \
    convertir_ijss_brut_vers_net = res

    # DONNEE
    res = specificites()
    complement, base_av_rup, pcts_base_av_rup, base_ap_rup, pcts_base_ap_rup, \
        type_deduction_recccn = res

    resultats = rule_ij_salaire_standard(
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
        type_deduction_recccn=type_deduction_recccn, debut=None, fin=None
    )

    si_erreur_lever_erreur(resultats)
    si_avertissement_lever_avertissement(resultats)
    message_debug("####################")
    message_debug(resultats)
    message_debug("####################")
    return resultats

return ij_classique() # DECOMMENTER SOUS COOG

####################
# FIN IJ CLASSIQUE #
