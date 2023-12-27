# ---
# Name: Indemnité Journalière selon motif et enfant (nouveau)
# Short Name: ij_salaire_tranche_motif_enfant_2018
# Type: benefit
# ---

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
# DEBUT IJ MOTIF X ENFANT #
###########################

###########################
# DEBUT IJ PALIER X MOTIF #
###########################

def selecteur_motif_vers_valeur(valeur_mat, valeur_acc_pro, valeur_acc_vp, valeur_mal_pro, valeur_mal_ord, motif):
    correspondance_motif_valeur = {
        'maternite': valeur_mat,
        'accident_du_travail': valeur_acc_pro,
        'accident': valeur_acc_vp,
        'maladie_professionnelle': valeur_mal_pro,
        'maladie': valeur_mal_ord
    }

    return correspondance_motif_valeur.get(motif)


#########################
# FIN IJ MOTIF X ENFANT #
# DEBUT IJ MOTIF X ENFANT #
###########################

def enfant_vers_pcts(intervalles, pcts_enfant, nb_enfant):
    res_pct = '0/0/0'
    found = False
    for index, intervalle in enumerate(intervalles):
        if not found:
            # cas de l'intervalle [A,B]
            a, b = intervalle
            if a <= nb_enfant <= b:
                res_pct = pcts_enfant[index]
                found = True
        else:
            break
    if not found:
        message_erreur = 'Taux pour %s enfant(s) non définis.' % nb_enfant
        ajouter_erreur(message_erreur)
        return res_pct
    return res_pct


#########################
# FIN IJ MOTIF X ENFANT #
# DEBUT IJ MOTIF X ENFANT #
###########################
def ij_motif_enfant():

    def specificites_motif_enfant():
        '''
        :donnees:
            - motif_arret
        :return:
        :rtype: list[dict[str,any]]
        '''

        # Paramètres
        base_av_rup = param_a02a_base_av_rup()
        base_ap_rup = param_a03a_base_ap_rup()

        complement_mal_pro = param_a01b_en_complement_mal_pro()
        complement_mal_ord = param_a01b_en_complement_mal_ord()
        complement_acc_pro = param_a01b_en_complement_acc_pro()
        complement_acc_vp = param_a01b_en_complement_acc_vp()
        complement_mat = param_a01b_en_complement_mat()

        pct_base_av_rup_mal_pro_enfant = param_a02b_pcts_base_av_rup_mal_pro_enfant()  # TA/TB/TC
        pcts_base_av_rup_mal_ord_enfant = param_a02b_pcts_base_av_rup_mal_ord_enfant()
        pcts_base_av_rup_acc_pro_enfant = param_a02b_pcts_base_av_rup_acc_pro_enfant()
        pcts_base_av_rup_acc_vp_enfant = param_a02b_pcts_base_av_rup_acc_vp_enfant()
        pcts_base_av_rup_mat_enfant = param_a02b_pcts_base_av_rup_mat_enfant()

        pcts_base_ap_rup_mal_pro_enfant = param_a03b_pcts_base_ap_rup_mal_pro_enfant()  # TA/TB/TC$...
        pcts_base_ap_rup_mal_ord_enfant = param_a03b_pcts_base_ap_rup_mal_ord_enfant()
        pcts_base_ap_rup_acc_pro_enfant = param_a03b_pcts_base_ap_rup_acc_pro_enfant()
        pcts_base_ap_rup_acc_vp_enfant = param_a03b_pcts_base_ap_rup_acc_vp_enfant()
        pcts_base_ap_rup_mat_enfant = param_a03b_pcts_base_ap_rup_mat_enfant()

        # GESTION MOTIF
        motif_arret = code_de_l_evenement_du_prejudice()

        complement = selecteur_motif_vers_valeur(
            complement_mat, complement_acc_pro, complement_acc_vp, complement_mal_pro, complement_mal_ord, motif_arret)

        pcts_base_av_rup_enfant = selecteur_motif_vers_valeur(
            pcts_base_av_rup_mat_enfant, pcts_base_av_rup_acc_pro_enfant,
            pcts_base_av_rup_acc_vp_enfant, pct_base_av_rup_mal_pro_enfant,
            pcts_base_av_rup_mal_ord_enfant, motif_arret)

        pcts_base_ap_rup_enfant = selecteur_motif_vers_valeur(
            pcts_base_ap_rup_mat_enfant, pcts_base_ap_rup_acc_pro_enfant,
            pcts_base_ap_rup_acc_vp_enfant, pcts_base_ap_rup_mal_pro_enfant,
            pcts_base_ap_rup_mal_ord_enfant, motif_arret)

        # GESTION ENFANT
        classes_enfant = param_a01z_classes_enfant() # 0:1$2:5$6:+ -> ['0:1', ...]
        classes_enfant = classes_enfant.split(caractere_separateur_classes) # 0:1$2:5$6:+ -> ['0:1', ...]
        for i, classe in enumerate(classes_enfant):
            a, b = classe.split(caractere_separateur_inf_sup)
            a = Decimal(a)
            if b == '+':
                b = '99'
            b = Decimal(b)
            classes_enfant[i] = [a, b]

        pcts_base_av_rup_enfant = pcts_base_av_rup_enfant.split(caractere_separateur_classes) # %TA/%TB/%TC$%TA/%TB/%TC$...

        pcts_base_ap_rup_enfant = pcts_base_ap_rup_enfant.split(caractere_separateur_classes) # %TA/%TB/%TC$%TA/%TB/%TC$...

        nb_enfants_a_charge = compl_nombre_d_enfants_a_charge()
        if nb_enfants_a_charge is None:
            message_none = "Saisir un nombre d'enfants."
            ajouter_erreur(message_none)
            return

        pcts_base_av_rup = enfant_vers_pcts(classes_enfant, pcts_base_av_rup_enfant, nb_enfants_a_charge)
        pcts_base_ap_rup = enfant_vers_pcts(classes_enfant, pcts_base_ap_rup_enfant, nb_enfants_a_charge)

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
            param_a07_convertir_ijss_brut_vers_net()
    )
    if si_erreur_lever_erreur(res):
        return

    duree, prime, \
    lim_av_rup, pcts_lim_av_rup, rv_lim_av_rup, \
    lim_ap_rup, pcts_lim_ap_rup, rv_lim_ap_rup, \
    red_ib_mt, lim_mt, rv_lim_mt, \
    assiette, freq, indice, premiere, date_ref, nbj_rv, \
    convertir_ijss_brut_vers_net = res

    # SPECIF
    res = specificites_motif_enfant()
    if res is None:
        return
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

    return resultats

return ij_motif_enfant() # DECOMMENTER SOUS COOG

#########################
# FIN IJ MOTIF X ENFANT #
