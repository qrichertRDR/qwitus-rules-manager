# ---
# Name: Règle de calcul de la revalorisation standard
# Short Name: revalorisation_standard
# Type: benefit_revaluation
# ---

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
date_debut_prejudice = date_de_debut_du_prejudice()
mode_revalo = param_1_reval_mode()
salaire_journalier_base = salaire_journalier_de_base()
description = description_du_calcul_du_salaire()

# calcul de la date de premiere revalo
if param_2_date_de_reference() == 'DAT' or not date_fin_franchise():
    premiere_revalo = date_de_debut_du_prejudice()
else:
    premiere_revalo = ajouter_jours(date_fin_franchise(), 1)
    
if param_3_1ere_revalorisation() == 'nb_jour':
    premiere_revalo = ajouter_jours(premiere_revalo, param_4_nombre_de_jours())
elif param_3_1ere_revalorisation() == '1er_janvier_suivant_date_ref':
    premiere_revalo = datetime.date(premiere_revalo.year + 1, 1, 1)
elif param_3_1ere_revalorisation() == '1jour_mois_suivant_date_anniversaire':
    premiere_revalo = ajouter_annees(premiere_revalo, 1)
    premiere_revalo = ajouter_jours(premiere_revalo, 1)
elif param_3_1ere_revalorisation() == '1er_semestre_suivant_date_ref':
    premiere_revalo = premiere_revalo
elif param_3_1ere_revalorisation() == '1er_jour_du_7_eme_mois_suivant_date_anniversaire':
    premiere_revalo = ajouter_annees(premiere_revalo, 1)
    premiere_revalo = ajouter_mois(premiere_revalo, 7)
elif param_3_1ere_revalorisation() == '1er_janvier_suivant_date_reference_365_jours':
    premiere_revalo = ajouter_jours(premiere_revalo, 365)
    premiere_revalo = datetime.date(premiere_revalo.year + 1, 1, 1)

# calcul des dates de changement de revalo
dates = []
dates.append(premiere_revalo)
frequence_revalo = param_5_frequence_revalo()
if frequence_revalo == 'changement_taux':
    dates.extend(dates_changement_table(mode_revalo, 1, date_debut_periode, date_fin_periode))
elif frequence_revalo == 'date_anniversaire_1er_revalo':
     dates = dates.extend(dates_pivot(date_debut_periode, date_fin_periode, 'YEARLY', premiere_revalo.month, premiere_revalo.day))
elif frequence_revalo in ('01/01/YEARLY', '01/07/YEARLY'):
    frequence_revalo = '01/01/YEARLY'
    jour_synchro, mois_synchro, frequence = frequence_revalo.split('/')
    dates = dates.extend(dates_pivot(date_debut_periode, date_fin_periode, frequence, int(mois_synchro), int(jour_synchro)))

# calcul des sous périodes
periodes = sous_periodes(dates, date_debut_periode, date_fin_periode)

# calcul du montant pour chaque sous période
res = []
salaire_journalier_revalorise = salaire_journalier_base
initial_description = description
for period in periodes:     
    description = initial_description
    if period[0] < premiere_revalo:
        taux_revalo = 1
    else:
        
        ### SPECIFIQUE PARTENAIRE DEBUT
        
        if mode_revalo == 'AGIRC_ARRCO':
            if code_assureur() == 'PM000':
               mode_revalo = '000_AGIRC_ARRCO'
            if code_assureur() == 'PM001':
               mode_revalo = '001_AGIRC_ARRCO'
            if code_assureur() == 'PM003':
               mode_revalo = '003_AGIRC_ARRCO'
            if code_assureur() == 'PM004':
               mode_revalo = '004_AGIRC_ARRCO'
            if code_assureur() == 'PM007':
               mode_revalo = '007_AGIRC_ARRCO'
            if code_assureur() == 'PM011':
               mode_revalo = '011_AGIRC_ARRCO'
            if code_assureur() == 'PM015':
               mode_revalo = '015_AGIRC_ARRCO'
            if code_assureur() == 'PM020':
               mode_revalo = '020_AGIRC_ARRCO'
            if code_assureur() == 'PM022':
               mode_revalo = '022_AGIRC_ARRCO'
            if code_assureur() == 'PM032':
               mode_revalo = '032_AGIRC_ARRCO'
            if code_assureur() == 'PM044':
               mode_revalo = '044_AGIRC_ARRCO'
            if code_assureur() == 'PM045':
               mode_revalo = '045_AGIRC_ARRCO'
            if code_assureur() == 'PM056':
               mode_revalo = '056_AGIRC_ARRCO'
            if code_assureur() == 'PM060':
               mode_revalo = '060_AGIRC_ARRCO'
            if code_assureur() == 'PM064':
               mode_revalo = '064_AGIRC_ARRCO'
            if code_assureur() == 'PM069':
               mode_revalo = '069_AGIRC_ARRCO'
            if code_assureur() == 'PM099':
               mode_revalo = '099_AGIRC_ARRCO'
            if code_assureur() == 'PM105':
               mode_revalo = '105_AGIRC_ARRCO'
            if code_assureur() == 'PM118':
               mode_revalo = '118_AGIRC_ARRCO'
       
        if mode_revalo == 'AGIRC':
            taux_revalo = table_AGIRC(period[0]) / table_AGIRC(date_debut_prejudice)
        elif mode_revalo == 'ARRCO':
            taux_revalo = table_ARRCO(period[0]) / table_ARRCO(date_debut_prejudice)
        elif mode_revalo == 'AGIRC_ARRCO':
            taux_revalo = table_AGIRC_ARRCO(period[0]) / table_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '000_AGIRC_ARRCO':
            taux_revalo = table_000_AGIRC_ARRCO(period[0]) / table_000_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '001_AGIRC_ARRCO':
            taux_revalo = table_001_AGIRC_ARRCO(period[0]) / table_001_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '003_AGIRC_ARRCO':
            taux_revalo = table_003_AGIRC_ARRCO(period[0]) / table_003_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '004_AGIRC_ARRCO':
            taux_revalo = table_004_AGIRC_ARRCO(period[0]) / table_004_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '007_AGIRC_ARRCO':
            taux_revalo = table_007_AGIRC_ARRCO(period[0]) / table_007_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '011_AGIRC_ARRCO':
            taux_revalo = table_011_AGIRC_ARRCO(period[0]) / table_011_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '015_AGIRC_ARRCO':
            taux_revalo = table_015_AGIRC_ARRCO(period[0]) / table_015_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '020_AGIRC_ARRCO':
            taux_revalo = table_020_AGIRC_ARRCO(period[0]) / table_020_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '022_AGIRC_ARRCO':
            taux_revalo = table_022_AGIRC_ARRCO(period[0]) / table_022_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '032_AGIRC_ARRCO':
            taux_revalo = table_032_AGIRC_ARRCO(period[0]) / table_032_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '044_AGIRC_ARRCO':
            taux_revalo = table_044_AGIRC_ARRCO(period[0]) / table_044_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '045_AGIRC_ARRCO':
            taux_revalo = table_045_AGIRC_ARRCO(period[0]) / table_045_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '056_AGIRC_ARRCO':
            taux_revalo = table_056_AGIRC_ARRCO(period[0]) / table_056_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '060_AGIRC_ARRCO':
            taux_revalo = table_060_AGIRC_ARRCO(period[0]) / table_060_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '064_AGIRC_ARRCO':
            taux_revalo = table_064_AGIRC_ARRCO(period[0]) / table_064_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '069_AGIRC_ARRCO':
            taux_revalo = table_069_AGIRC_ARRCO(period[0]) / table_069_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '099_AGIRC_ARRCO':
            taux_revalo = table_099_AGIRC_ARRCO(period[0]) / table_099_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '105_AGIRC_ARRCO':
            taux_revalo = table_105_AGIRC_ARRCO(period[0]) / table_105_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '118_AGIRC_ARRCO':
            taux_revalo = table_118_AGIRC_ARRCO(period[0]) / table_118_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '022_KN_REVALO':
            taux_revalo = table_022_KN_REVALO(period[0]) / table_022_KN_REVALO(date_debut_prejudice)
        elif mode_revalo == '038_SMI_REVALO':
            taux_revalo = table_038_SMI_REVALO(period[0]) / table_038_SMI_REVALO(date_debut_prejudice)
        elif mode_revalo == '040_UNIP_REVALO':
            taux_revalo = table_040_UNIP_REVALO(period[0]) / table_040_UNIP_REVALO(date_debut_prejudice)
        elif mode_revalo == '043_APICIL_REVALO':
            taux_revalo = table_043_APICIL_REVALO(period[0]) / table_043_APICIL_REVALO(date_debut_prejudice)
        elif mode_revalo == '054_LMG_REVALO':
            taux_revalo = table_054_LMG_REVALO(period[0]) / table_054_LMG_REVALO(date_debut_prejudice)
        elif mode_revalo == '056_GENERALI_REVALO':
            taux_revalo = table_056_GENERALI_REVALO(period[0]) / table_056_GENERALI_REVALO(date_debut_prejudice)
        elif mode_revalo == '056_GENERALI_REVALO_20SAL':
            taux_revalo = table_056_GENERALI_REVALO_20SAL(period[0]) / table_056_GENERALI_REVALO_20SAL(date_debut_prejudice)
        elif mode_revalo == '059_KLESIA_PREV_REVALO':
            taux_revalo = table_059_KLESIA_PREV_REVALO(period[0]) / table_059_KLESIA_PREV_REVALO(date_debut_prejudice)
        elif mode_revalo == '063_CARCEPT_REVALO':
            taux_revalo = table_063_CARCEPT_REVALO(period[0]) / table_063_CARCEPT_REVALO(date_debut_prejudice)
        elif mode_revalo == '065_GROUPAMA_ALSACE_REVALO':
            taux_revalo = table_065_GROUPAMA_ALSACE_REVALO(period[0]) / table_065_GROUPAMA_ALSACE_REVALO(date_debut_prejudice)
        elif mode_revalo == '067_GRESHAM_REVALO':
            taux_revalo = table_067_GRESHAM_REVALO(period[0]) / table_067_GRESHAM_REVALO(date_debut_prejudice)
        elif mode_revalo == '083_IDMUT_REVALO':
            taux_revalo = table_083_IDMUT_REVALO(period[0]) / table_083_IDMUT_REVALO(date_debut_prejudice)
        elif mode_revalo == '085_IDMUT_REVALO':
            taux_revalo = table_085_IDMUT_REVALO(period[0]) / table_085_IDMUT_REVALO(date_debut_prejudice)
        elif mode_revalo == '087_KLESIA_PREV_REVALO':
            taux_revalo = table_087_KLESIA_PREV_REVALO(period[0]) / table_087_KLESIA_PREV_REVALO(date_debut_prejudice)
        elif mode_revalo == '110_SMAVIE_REVALO':
            taux_revalo = table_110_SMAVIE_REVALO(period[0]) / table_110_SMAVIE_REVALO(date_debut_prejudice)
        elif mode_revalo == '117_ARPEGE_REVALO':
            taux_revalo = table_117_ARPEGE_REVALO(period[0]) / table_117_ARPEGE_REVALO(date_debut_prejudice)
        
        ### SPECIFIQUE PARTENAIRE FIN
        

    salaire_journalier_revalorise = arrondir(salaire_journalier_base * taux_revalo, 0.01)
    if (salaire_journalier_revalorise - salaire_journalier_base) != 0.0:
        description += 'Montant de la revalorisation: %s€\n' % (salaire_journalier_revalorise - salaire_journalier_base)
    nb_jour = (period[1] - period[0]).days + 1
    description += 'Montant total: %s€ * %s = %s€' % (salaire_journalier_revalorise, nb_jour,
        nb_jour * salaire_journalier_revalorise)
    res.append({
            'start_date': period[0],
            'end_date': period[1],
            'nb_of_unit': (period[1] - period[0]).days + 1,
            'unit': 'day',
            'amount': ((period[1] - period[0]).days + 1) * salaire_journalier_revalorise,
            'amount_per_unit': salaire_journalier_revalorise,
            'base_amount': salaire_journalier_base,
            'description': description,
            'date_limite': None,
            })
return res
