# ---
# Name: Revalorisation (nouveau, privée)
# Short Name: revalorisation_privee
# Type: tool
# ---

# DEBUT RV2 STANDARD #
######################

# RV2 STANDARD (POUR OUTILLAGE)
def switch_date_reference(date_reference, dat, dei):

    if date_reference is None:
        message = 'Date de référence absente.'
        ajouter_avertissement(message)
        return message

    date_reference = date_reference.upper()
    dict_date_reference = {
        'DAT':
            (dat, "début d'arrêt de travail"),
        'DEI':
            (dei, "effet d'indemnisation"),
        # 'selon_cg': None  # TODO
    }

    res = dict_date_reference.get(
        date_reference, 'Date de référence invalide : %s.' % date_reference
    )

    if isinstance(res, str):
        ajouter_avertissement(res)
        return res

    return res


def switch_premiere_revalorisation(type_date, date_ref, nb_jour):

    type_date = type_date.upper()
    plus_365_j = ajouter_jours(date_ref, 365)
    plus_365_j_et_1_m = ajouter_mois(plus_365_j, 1)
    plus_1_m = ajouter_mois(date_ref, 1)
    plus_7_m = ajouter_mois(date_ref, 7)
    plus_1_s = ajouter_semestres(date_ref, 1)  # vérifier
    plus_365_j_et_1_s = ajouter_semestres(plus_365_j, 1)
    plus_6_m = ajouter_mois(date_ref, 6)

    dict_premiere_revalorisation = {
        'NB_JOUR': ajouter_jours(
            date_ref, nb_jour
        ),
        '01/01': datetime.date(
            date_ref.year + 1, 1, 1
        ),
        '01/01+365J': datetime.date(
            plus_365_j.year + 1, 1, 1
        ),
        '01/07': datetime.date(
            date_ref.year + (0 if date_ref.month < 7 else 1), 7, 1
        ),
        '01/07+365J': datetime.date(
            plus_365_j.year + (0 if date_ref.month < 7 else 1), 7, 1
        ),
        '01/+1M': datetime.date(
            plus_1_m.year, plus_1_m.month, 1
        ),
        '01/+1M+365J': datetime.date(
            plus_365_j_et_1_m.year, plus_365_j_et_1_m.month, 1
        ),
        '01/+7M': datetime.date(
            plus_7_m.year, plus_7_m.month, 1
        ),
        '01/+SEM': datetime.date(
            plus_1_s.year, plus_1_s.month, 1
        ),
        '01/+SEM+365J': datetime.date(
            plus_365_j_et_1_s.year, plus_365_j_et_1_s.month, 1
        ),
        '+6M': plus_6_m,
        'SANS_DELAI': date_ref,
        # '01/07_si_presta_avant_01/01': None,  # TODO
        # 'selon_cg': None # TODO
        # switch_premiere_revalorisation(table_cg(date), date_ref)  # TODO
    }

    res = dict_premiere_revalorisation.get(
        type_date, 'Type de date invalide : %s' % type_date
    )

    if isinstance(res, str):
        ajouter_avertissement(res)
        return res

    return res


def switch_frequence(frequence, debut, fin, prem_rv, indice, dat):

    frequence = frequence.upper()
    indice = indice.upper()
    indice = _get_new_indice(indice)

    prem_trimestriel = [x for x in dates_pivot(dat, fin, 'MONTHLY', 1, 1)
                        if x.month in [1, 4, 7, 10]]

    prem_rv_annuel = [prem_rv]
    while True:
        date_suivante = prem_rv_annuel[-1] + relativedelta(years=1)
        if date_suivante <= fin:
            prem_rv_annuel.append(date_suivante)
        else:
            break

    prem_jan_annuel = [x for x in dates_pivot(dat, fin, 'YEARLY', 1, 1)]
    # if x >= debut]
    prem_jui_annuel = [x for x in dates_pivot(dat, fin, 'YEARLY', 7, 1)]
    # if x >= debut]
    prem_oct_annuel = [x for x in dates_pivot(dat, fin, 'YEARLY', 10, 1)]
    # if x >= debut]

    prem_jan_jui_annuel = list(prem_jan_annuel)
    prem_jan_jui_annuel.extend(prem_jui_annuel)

    # TS35
    infini = datetime.date.max
    cgts_taux = dates_changement_table(indice, 1, debut, infini)
    cgts_taux = [x for x in cgts_taux if debut <= x <= fin]

    dict_frequence = {
        '01/01/ANNUEL': prem_jan_annuel,
        '01/07/ANNUEL': prem_jui_annuel,
        '01/01_07/ANNUEL': prem_jan_jui_annuel,
        '01/10/ANNUEL': prem_oct_annuel,
        'CHANGEMENT_TAUX': cgts_taux,
        'DATE_ANNIVERSAIRE_1ER_REVALO': prem_rv_annuel,
        'TRIMESTRIEL': prem_trimestriel,
        'D0101': prem_jan_annuel,
        # 'date_choisie_ca': None,  # TODO
        # 'selon_cg': None  # TODO
    }

    res = dict_frequence.get(
        frequence, 'Type de fréquence invalide : %s' % frequence
    )

    if isinstance(res, str):
        ajouter_avertissement(res)
        return res

    res.sort()

    return res
 
def _get_new_indice(indice) -> str:
    ### SPECIFIQUE PARTENAIRE DEBUT
    agirc_arrco_assureur = ['PM000', 'PM001', 'PM003', 'PM004', 'PM007',
        'PM011', 'PM015', 'PM020', 'PM022', 'PM032', 'PM044', 'PM045', 'PM056',
        'PM060', 'PM064', 'PM069', 'PM099', 'PM105', 'PM118']
    if indice == 'AGIRC_ARRCO':
        if code_assureur() in agirc_arrco_assureur:
            indice = code_assureur()[2:6]+'_AGIRC_ARRCO'
    return indice
    ### SPECIFIQUE PARTENAIRE FIN

def switch_indice(indice, date):

    indice = indice.upper()
    ### SPECIFIQUE PARTENAIRE DEBUT
    indice = _get_new_indice(indice)

    dict_indice = {
        'AGIRC': table_AGIRC(date),
        'ARRCO': table_ARRCO(date),
        'AGIRC_ARRCO': table_AGIRC_ARRCO(date),
        '000_AGIRC_ARRCO': table_000_AGIRC_ARRCO(date),
        '001_AGIRC_ARRCO': table_001_AGIRC_ARRCO(date),
        '003_AGIRC_ARRCO': table_003_AGIRC_ARRCO(date),
        '004_AGIRC_ARRCO': table_004_AGIRC_ARRCO(date),
        '007_AGIRC_ARRCO': table_007_AGIRC_ARRCO(date),
        '011_AGIRC_ARRCO': table_011_AGIRC_ARRCO(date),
        '015_AGIRC_ARRCO': table_015_AGIRC_ARRCO(date),
        '020_AGIRC_ARRCO': table_020_AGIRC_ARRCO(date),
        '022_AGIRC_ARRCO': table_022_AGIRC_ARRCO(date),
        '032_AGIRC_ARRCO': table_032_AGIRC_ARRCO(date),
        '044_AGIRC_ARRCO': table_044_AGIRC_ARRCO(date),
        '045_AGIRC_ARRCO': table_045_AGIRC_ARRCO(date),
        '056_AGIRC_ARRCO': table_056_AGIRC_ARRCO(date),
        '060_AGIRC_ARRCO': table_060_AGIRC_ARRCO(date),
        '064_AGIRC_ARRCO': table_064_AGIRC_ARRCO(date),
        '069_AGIRC_ARRCO': table_069_AGIRC_ARRCO(date),
        '099_AGIRC_ARRCO': table_099_AGIRC_ARRCO(date),
        '105_AGIRC_ARRCO': table_105_AGIRC_ARRCO(date),
        '118_AGIRC_ARRCO': table_118_AGIRC_ARRCO(date),
        '022_KN_REVALO': table_022_KN_REVALO(date),
        '038_SMI_REVALO': table_038_SMI_REVALO(date),
        '040_UNIP_REVALO': table_040_UNIP_REVALO(date),
        '043_APICIL_REVALO': table_043_APICIL_REVALO(date),
        '054_LMG_REVALO': table_054_LMG_REVALO(date),
        '056_GENERALI_REVALO': table_056_GENERALI_REVALO(date),
        '056_GENERALI_REVALO_20SAL': table_056_GENERALI_REVALO_20SAL(date),
        '059_KLESIA_PREV_REVALO': table_059_KLESIA_PREV_REVALO(date),
        '063_CARCEPT_REVALO': table_063_CARCEPT_REVALO(date),
        '065_GROUPAMA_ALSACE_REVALO': table_065_GROUPAMA_ALSACE_REVALO(date),
        '067_GRESHAM_REVALO': table_067_GRESHAM_REVALO(date),
        '083_IDMUT_REVALO': table_083_IDMUT_REVALO(date),
        '085_IDMUT_REVALO': table_085_IDMUT_REVALO(date),
        '087_KLESIA_PREV_REVALO': table_087_KLESIA_PREV_REVALO(date),
        '110_SMAVIE_REVALO': table_110_SMAVIE_REVALO(date),     
        '117_ARPEGE_REVALO': table_117_ARPEGE_REVALO(date),     
        'GAN': table_GAN(date),
        'IM': table_IM(date),
        'TBZ': table_TBZ(date),
        'UNIRS': table_UNIRS(date),
        'OREPA': table_OREPA(date),
        # 'selon_ccn' : switch_indice(table_ccn(date)),  # TODO
        # 'selon_cp' : switch_indice(table_cp(date)),  # TODO
        # 'selon_ca' : switch_indice(table_ca(date)),  # TODO
        # 'selon_cg': switch_indice(table_CG(date))  # TODO
    }

    ### SPECIFIQUE PARTENAIRE FIN

    res = dict_indice.get(
        indice,
        'Indice ou date invalide : (%s, %s)' % (indice, formater_date(date))
    )

    if isinstance(res, str):
        ajouter_avertissement(res)
        return res

    return res


# PLACER DANS UNE REGLE revalorisation_privee SOUS COOG
def rule_revalorisation_privee(debut, fin, indice, date_reference,
                               premiere_revalorisation, frequence,
                               nombre_jours, montant_journalier,
                               inversion=False, periodes=None, precision=0.01):

    # Si périodes de revalorisation fournies :
    #    valeurs réelles des indices
    # Sinon
    #    valeurs contractuelles des indices
    # Le taux utilisé n'est pas arrondi

    def description_revalorisation(dsp, fsp, cp, date_prem_revalo, taux,
                                   coef_cp, inversion, coef_pivot, revalorise,
                                   montant):

        desc_periode = ''
        if montant <= 0:
            return desc_periode

        # DATE DE PREMIERE REVALORISAION EN RENTE AVEC REVALO INITIALE ? OUI
        if dsp < date_prem_revalo:
            desc_periode += '\nTaux : %s ' \
                                   '(avant première revalorisation)\n' % taux
        else:
            # date de calcul du point < première plage d'indice
            if coef_cp is None:
                desc_periode += '\nTaux : %s ' \
                                       "(avant plage d'indice)\n" % taux
            # date de calcul du point >= première plage d'indice
            else:
                if not inversion:
                    desc_periode += '\nTaux : %.4f = %.4f / %.4f\n' \
                                       % (taux, coef_cp, coef_pivot)
                else:
                    desc_periode += '\nTaux : %.4f = %.4f / %.4f\n' \
                                           % (taux, coef_pivot, coef_cp)

                desc_periode += 'Le montant %srevalorisé est de %s€\n' \
                                % ('non ' if inversion
                                   else '',
                                   revalorise)

        return desc_periode


    description = '\n'
    description += 'RV STANDARD\n'
    description += 'Période : du %s au %s\n' \
                   % (formater_date(debut), formater_date(fin))
    description += "Selon l'indice : %s\n" % indice
    description += 'A une fréquence : %s\n' % frequence
    description += 'Depuis : %s %s\n' % (
        date_reference,
        premiere_revalorisation if nombre_jours is None
        else ('+ '
              + str(nombre_jours)
              + ' jour(s)'
              )
    )

    # DATE DE REFERENCE
    dat = date_debut_arret_de_travail()
    ei = ajouter_jours(date_fin_franchise(), 1)
    res_date_reference = switch_date_reference(
        date_reference=date_reference, dat=dat, dei=ei
    )

    if isinstance(res_date_reference, str):
        return {'erreur': res_date_reference}

    date_reference, desc_date_reference = res_date_reference
    description += ' | Date de référence : %s %s' % \
                   (desc_date_reference, formater_date(date_reference))

    # DATE DE PREMIERE REVALORISATION
    date_prem_revalo = switch_premiere_revalorisation(
        type_date=premiere_revalorisation, date_ref=date_reference,
        nb_jour=nombre_jours
    )

    if isinstance(date_prem_revalo, str):
        return {'erreur': date_prem_revalo}

    description += ' | Première revalo : %s' % formater_date(date_prem_revalo)

    derniere_revalo_ass_prec = None
    if periodes is None:

        # DATES DE REVALORISATION
        dates = [date_prem_revalo]
        res_frequence = switch_frequence(
            frequence=frequence, debut=dat, fin=fin, prem_rv=date_prem_revalo,
            indice=indice, dat=dat
        )

        if isinstance(res_frequence, str):
            return {'erreur': res_frequence}

        # DEBUT CGT ASSUREUR
        res_sortie_contrat = rule_cgt_gestion_contrat()
        if res_sortie_contrat is None:
            return {'erreur':
                        'Erreur de gestion de contrat '
                        "pour un changement d'assureur"}

        _, regle_sortie, _, date_sortie, exception = res_sortie_contrat
        if regle_sortie is not None and date_sortie is not None:
            if regle_sortie == 'lock_indemnifications':
                res_frequence = [x for x in res_frequence if
                                 x == fin or (x != fin and x <= date_sortie)]

                '''
                ATTENTION : CGT ASSUREUR ASS N > ASS N+1
                - contexte d'ASS N 
                - nouvel évènement couvert par ASS N 
                - après sortie d'ASS N
                
                Si on dépasse la 1RV du nouvel evt, la date de revalorisation
                à retenir pour ASS 1 est la dernière <= sortie d'ASS N.
                '''

                # nouvel evt couvert par l'assureur précédent après sa sortie
                if exception:
                    # dates de revalo contrat avant sortie de l'assureur préc.
                    if res_frequence is not None:
                        if len(res_frequence) == 0:
                            # ne pas revaloriser
                            derniere_revalo_ass_prec = dat
                        else:
                            # HOTFIX liste non triée
                            derniere_revalo_ass_prec = max(res_frequence)

        # FIN CGT ASSUREUR

        dates.extend(res_frequence)
        # HOTFIX NBO21 sous_periodes (début > fin si dates dupliquées)
        dates = list(set(dates))

        # PERIODES DE REVALORISATION
        if len(dates) > 0:
            description += '\nDates de revalorisation : '
            for date in dates:
                description += '%s ' % formater_date(date)

        description += '\nSous-périodes : '
        periodes = sous_periodes(dates, dat, fin)

    # CALCUL DES SOUS PERIODES
    res = []

    # PIVOT
    coef_pivot = switch_indice(indice, dat)
    coef_cp = None
    if isinstance(coef_pivot, str):
        return {'erreur': coef_pivot}

    for dsp, fsp in periodes:
        cp = dsp

        # DERNIERE REVALO ASSUREUR PRECEDENT
        if derniere_revalo_ass_prec:
            cp = derniere_revalo_ass_prec

        # FREQUENCE D0101
        if frequence.upper() == 'D0101':
            cp = datetime.date(cp.year - 1, 7, 1)

        # passer si début de période non atteint
        if debut > fsp:
            continue

        # recaler
        if debut > dsp:
            dsp = debut

        # DATE DE PREMIERE REVALORISAION EN RENTE AVEC REVALO INITIALE ? OUI
        if dsp < date_prem_revalo:
            taux = 1
        else:
            coef_cp = switch_indice(indice, cp)

            if isinstance(coef_cp, str):
                return {'erreur': coef_cp}

            # date de calcul du point < première plage d'indice
            if coef_cp is None:
                taux = 1
            # date de calcul du point >= première plage indice
            else:
                # début arrêt de travail < première plage indice
                if coef_pivot is None:
                    # remplacer par le coefficient de calcul de point
                    coef_pivot = coef_cp

                taux = coef_cp / coef_pivot
                if inversion:
                    taux = 1 / taux

        revalorise = montant_journalier

        # on réduit le montant (même négatif) car taux - 1 négatif
        if inversion and taux <= 1:
            revalorise += (taux - 1) * abs(montant_journalier)
        # on augmente le montant (même négatif) car taux - 1 positif
        elif not inversion and taux >= 1:
            revalorise += (taux - 1) * abs(montant_journalier)
        else:
            if inversion:
                message_erreur = 'Montant dévalorisé %s supérieur ' \
                                 'au montant de base %s.' % \
                                 (revalorise, montant_journalier)
            else:
                message_erreur = 'Montant revalorisé %s inférieur ' \
                                 'au montant de base %s.' % \
                                 (revalorise, montant_journalier)

            ajouter_avertissement(message_erreur)
            return {'erreur': message_erreur}

        revalorise = arrondir(revalorise, precision)

        description_periode = description_revalorisation(
            dsp=dsp, fsp=fsp, cp=cp, date_prem_revalo=date_prem_revalo,
            taux=taux, coef_cp=coef_cp, inversion=inversion,
            coef_pivot=coef_pivot, revalorise=revalorise,
            montant=montant_journalier
        )

        res_periode = {
            'start_date': dsp,
            'end_date': fsp,
            'base_amount': revalorise,
            'description': description_periode,
            'date_limite': None,
            'taux': taux
        }
        res.append(res_periode)
        description += description_periode

    ajouter_info(description)
    return res, description


def revalorisation():
    ajouter_info('RV1')
    ind = param_indice()
    freq = param_frequence()
    prem_rv = param_premiere_revalorisation()
    date_ref = param_date_reference()
    nb_j = param_nombre_jours()
    montant_j = param_montant_journalier()
    debut = param_debut()
    fin = param_fin()
    inversion = param_inversion()
    periodes = param_periodes()
    return rule_revalorisation_privee(
        debut=debut, fin=fin, indice=ind, date_reference=date_ref,
        premiere_revalorisation=prem_rv, frequence=freq, nombre_jours=nb_j,
        montant_journalier=montant_j, periodes=periodes, inversion=inversion
    )

return revalorisation() # DECOMMENTER SOUS COOG

####################
# FIN RV2 STANDARD #
