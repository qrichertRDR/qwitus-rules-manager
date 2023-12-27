# ---
# Name: Calcul du salaire NET (A payer)
# Short Name: net_salary_calculation_a_payer
# Type: benefit_net_salary_calculation
# ---

# DEBUT NET A PAYER #
#####################

####################
# DEBUT NET FISCAL #
####################

#############
# DEBUT NET #
#############

def salaire_type_net(type_net, gerer_prime=True):

    ############################################################
    # FONCTION DE CALCUL DU SALAIRE NET FISCAL OU A PAYER      #
    # 1 - RECUPERATION DES TAUX OU MONTANTS DE COTISATIONS     #
    # 2 - RECUPERATION DES ASSIETTES                           #
    # 3 - DEDUCTIONS DES COTISATIONS                           #
    ############################################################

    # NET A PAYER OU FISCAL
    net_a_payer = type_net == 'net_a_payer'

    # CONTRIBUTIONS COMMUNES NET A PAYER OU FISCAL (URRSAF, RETRAITE, PREV, CHOMAGE)
    ## TAUX
    contrib_salariales = [
        '1_urssaf_1', '1_urssaf_2', '1_urssaf_3', '1_urssaf_4',
        '2_retraite_1', '2_retraite_2',
        '3_prevoyance_1', '3_prevoyance_2',
        '4_chomage_1', '4_chomage_2',
    ]

    taux_a_sal = taux_de_la_tranche('A', fixed=False, codes_list=contrib_salariales) or 0
    taux_b_sal = taux_de_la_tranche('B', fixed=False, codes_list=contrib_salariales) or 0
    taux_c_sal = taux_de_la_tranche('C', fixed=False, codes_list=contrib_salariales) or 0
    taux_d_sal = taux_c_sal # vu avec Joel: on utilise les taux de contributions de la tranche TC pour la tranche TD

    if (taux_a_sal + taux_b_sal + taux_c_sal + taux_d_sal) > 0:

        # CONTRIBUTION SPECIFIQUE NET A PAYER (MUTUELLE)
        ## TAUX OU MONTANT
        montant_contrib_sal_mutuelle = 0
        if net_a_payer:
            contrib_sal_mutuelle = ['51_charges_salariales_mutuelle_73']
            taux_a_sal_mut = taux_de_la_tranche('A', fixed=False, codes_list=contrib_sal_mutuelle) or 0
            taux_b_sal_mut = taux_de_la_tranche('B', fixed=False, codes_list=contrib_sal_mutuelle) or 0
            taux_c_sal_mut = taux_de_la_tranche('C', fixed=False, codes_list=contrib_sal_mutuelle) or 0
            taux_d_sal_mut = taux_c_sal_mut

            taux_a_sal += taux_a_sal_mut
            taux_b_sal += taux_b_sal_mut
            taux_c_sal += taux_c_sal_mut
            taux_d_sal += taux_d_sal_mut

            contrib_sal_mutuelle_en_taux = (taux_a_sal_mut + taux_b_sal_mut + taux_c_sal_mut + taux_d_sal_mut) > 0
            if not contrib_sal_mutuelle_en_taux:
                contrib_sal_mutuelle = ['1_charges_salariales_mutuelle']
                montant_contrib_sal_mutuelle = taux_de_la_tranche(fixed=True, codes_list=contrib_sal_mutuelle) or 0

        # CSG DEDUCTIBLE (NET A PAYER OU FISCAL), CSG NON DEDUCTIBLE ET RDS (SI NET A PAYER)
        ## TAUX (cgt taux csg deductible 0.051 -> 0.068 pour les AT après le 31/01/2018)
        debut_arret_travail = date_debut_arret_de_travail()
        date_limite = datetime.date(2018, 2, 1)
        csg_deductible, csg_non_deductible, rds = 0.051, 0.024, 0.005
        if debut_arret_travail >= date_limite:
            csg_deductible = 0.068
        tauxcsgrds = csg_deductible + (csg_non_deductible if net_a_payer else 0) + (rds if net_a_payer else 0)

        # ASSIETTE SALAIRE BRUT AVEC PRIME
        if gerer_prime:
               tranches = tranche_salaire(['gross_salary', 'salary_bonus'])
        else:
               tranches = tranche_salaire(['gross_salary'])

        TRA, TRB, TRC, TRD = tranches['TA'], tranches['TB'], tranches['TC'], 0
        salaire_brut_prime = TRA + TRB + TRC

        # ASSIETTE CSG/RDS
        ## BASE SALAIRE
        assiette_csg_rds = 0.9825 * salaire_brut_prime

        ## BASE CHARGES PATRONALES
        ### PREVOYANCE
        contrib_pat_prev = ['5_charges_patronales_prevoyance']
        taux_a_prev = taux_de_la_tranche('A', fixed=False, codes_list=contrib_pat_prev) or 0
        taux_b_prev = taux_de_la_tranche('B', fixed=False, codes_list=contrib_pat_prev) or 0
        taux_c_prev = taux_de_la_tranche('C', fixed=False, codes_list=contrib_pat_prev) or 0
        taux_d_prev = taux_c_prev
        contrib_pat_prev_en_taux = (taux_a_prev + taux_b_prev + taux_c_prev + taux_d_prev) > 0

        if not contrib_pat_prev_en_taux:
            message_debug('Contribution patronale prévoyance non exprimée.')
        else:
            assiette_csg_rds += (taux_a_prev * TRA + taux_b_prev * TRB + taux_c_prev * TRC + taux_d_prev * TRD) / 100

        ### SANTE
        contrib_pat_sante_taux = ['6_charges_patronales_sante_taux']
        taux_a_sante = taux_de_la_tranche('A', fixed=False, codes_list=contrib_pat_sante_taux) or 0
        taux_b_sante = taux_de_la_tranche('B', fixed=False, codes_list=contrib_pat_sante_taux) or 0
        taux_c_sante = taux_de_la_tranche('C', fixed=False, codes_list=contrib_pat_sante_taux) or 0
        taux_d_sante = taux_c_sante
        contrib_pat_sante_en_taux = (taux_a_sante + taux_b_sante + taux_c_sante + taux_d_sante) > 0

        if not contrib_pat_sante_en_taux:
            contrib_pat_sante_montant = ['2_charges_patronales_sante_montant']
            montant_sante = taux_de_la_tranche(fixed=True, codes_list=contrib_pat_sante_montant) or 0
            assiette_csg_rds += montant_sante
        else:
            assiette_csg_rds += (taux_a_sante * TRA + taux_b_sante * TRB + taux_c_sante * TRC + taux_d_sante * TRD) / 100

        # CALCUL DU NET
        salaire_net = salaire_brut_prime

        # DEDUCTION URRSAF, RETRAITE, PREV, CHOMAGE (NET A PAYER OU FISCAL) ET MUTUELLE (SI NET A PAYER)
        salaire_net -= (TRA * taux_a_sal + TRB * taux_b_sal + TRC * taux_c_sal + TRD * taux_d_sal) / 100
        salaire_net -= montant_contrib_sal_mutuelle # nul si taux mutuelle saisis

        # DEDUCTION CSG DED (NET A PAYER OU FISCAL) CSG NON DED ET RDS (SI NET A PAYER)
        salaire_net -= assiette_csg_rds * tauxcsgrds
        return arrondir(salaire_net, 0.01)
    else:
        return 0


###########
# FIN NET #
###########


def salaire_net_a_payer():
    '''
    Nom : Calcul du salaire NET (A payer)
    Code : net_salary_calculation_a_payer
    Type : Prestation: Calcul du salaire net
    Type du résultat :
    Contexte : Context par défaut
    Statut : Validé
    '''
    net_sans_prime = salaire_type_net('net_a_payer', False)
    net_avec_prime = salaire_type_net('net_a_payer')
    prime_net = net_avec_prime - net_sans_prime
    return net_sans_prime, prime_net

return salaire_net_a_payer() # DECOMMENTER NET A PAYER


###################
# FIN NET A PAYER #
