# ---
# Name: IJ Paramètres Génériques
# Short Name: ij_parametres_generiques
# Type: tool
# ---

# DEBUT IJ PARAMETRE GENERIQUE #
################################

def parametres_generiques():
    '''
    .. todo :: Externaliser dans un autre fichier
    '''
    return rule_ij_parametres_generiques(
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


def rule_ij_parametres_generiques(
        a01a_duree_presta, a01c_prime, a02c_lim_av_rup, a02d_pcts_lim_av_rup,
        a02e_rv_lim_av_rup, a03c_lim_ap_rup, a03d_pcts_lim_ap_rup,
        a03e_rv_lim_ap_rup, a04a_red_ib_mt, a04b_lim_mt, a04c_rv_lim_mt,
        a05a_assiette_rv, a05b_freq_rv, a05c_indice_rv, a05d_premiere_rv,
        a05e_date_ref_rv, a05f_nbj_rv, a07_convertir_ijss_brut_vers_net
    ):
    '''
    .. todo :: Utiliser les paramètres de fonction plutôt que les fonctions
               `param_*`.
    '''
    # GENERAL
    duree = param_a01a_duree_presta()
    prime = param_a01c_prime()

    # TESTS
    if duree is None:
        message_none = 'Durée de prestation non renseignée.'
        message_debug(message_none)
        return {'erreur': message_none}

    if prime is None:
        message_none = 'Prime de référence non renseignée.'
        message_debug(message_none)
        return {'erreur': message_none}

    # AVANT RUPTURE
    lim_av_rup = param_a02c_lim_av_rup()
    pcts_lim_av_rup = param_a02d_pcts_lim_av_rup()
    rv_lim_av_rup = param_a02e_rv_lim_av_rup()

    if lim_av_rup is None:
        message = 'Limite avant rupture non renseignée.'
        message_debug(message)
        return {'erreur': message}
    else:
        if lim_av_rup in ['',
                          'non']:
            if rv_lim_av_rup:
                message = 'Paramètrage KO : limite avant rupture désactivée mais revalorisation activée.'
                message_debug(message)
                return {'erreur': message}

    # APRES RUPTURE
    lim_ap_rup = param_a03c_lim_ap_rup()
    pcts_lim_ap_rup = param_a03d_pcts_lim_ap_rup()
    rv_lim_ap_rup = param_a03e_rv_lim_ap_rup()

    if lim_ap_rup is None:
        message = 'Limite après rupture non renseignée.'
        message_debug(message)
        return {'erreur': message}
    else:
        if lim_ap_rup in ['',
                          'non']:
            if rv_lim_ap_rup:
                message = 'Paramètrage KO : ' \
                          'limite après rupture désactivée ' \
                          'mais revalorisation activée.'
                message_debug(message)
                return {'erreur': message}

    # MI TEMPS
    red_ib_mt = param_a04a_red_ib_mt()
    lim_mt = param_a04b_lim_mt()
    rv_lim_mt = param_a04c_rv_lim_mt()

    # TESTS
    if red_ib_mt is None:
        message = "Réduction de l'indemnité de base non renseignée."
        message_debug(message)
        return {'erreur': message}

    if lim_mt is None:
        message = 'Limite de mi-temps non renseignée.'
        message_debug(message)
        return {'erreur': message}

    if rv_lim_mt is None:
        message = 'Revalorisation de lim de mi-temps non renseignée.'
        message_debug(message)
        return {'erreur': message}

    # REVALO
    assiette = param_a05a_assiette_rv()
    freq = param_a05b_freq_rv()
    indice = param_a05c_indice_rv()
    premiere = param_a05d_premiere_rv()
    date_ref = param_a05e_date_ref_rv()
    nbj_rv = param_a05f_nbj_rv()

    if assiette is None:
        message = 'Assiette revalorisation non renseignée.'
        message_debug(message)
        return {'erreur': message}

    if freq is None:
        message = 'Frequence revalorisation non renseignée.'
        message_debug(message)
        return {'erreur': message}

    if indice is None:
        message = 'Indice de revalorisation non renseigné.'
        message_debug(message)
        return {'erreur': message}

    if premiere is None:
        message = 'Première revalorisation non renseignée.'
        message_debug(message)
        return {'erreur': message}

    if date_ref is None:
        message = 'Date de référence revalorisation non renseignée.'
        message_debug(message)
        return {'erreur': message}

    if nbj_rv is None:
        if premiere == 'nb_jour':
            message = 'Nombre de jours revalorisation non renseigné.'
            message_debug(message)
            return {'erreur': message}
        else:
            nbj_rv = 0

    convertir_ijss_brut_vers_net = param_a07_convertir_ijss_brut_vers_net()
    if convertir_ijss_brut_vers_net is None:
        message = "Conversion de l'ijss brut en ijss net non renseignée."
        message_debug(message)
        return {'erreur': message}


    return duree, prime, \
           lim_av_rup, pcts_lim_av_rup, rv_lim_av_rup, \
           lim_ap_rup, pcts_lim_ap_rup, rv_lim_ap_rup,\
           red_ib_mt, lim_mt, rv_lim_mt,\
           assiette, freq, indice, premiere, date_ref, nbj_rv,\
           convertir_ijss_brut_vers_net

return parametres_generiques() # DECOMMENTER SOUS COOG

##############################
# FIN IJ PARAMETRE GENERIQUE #
