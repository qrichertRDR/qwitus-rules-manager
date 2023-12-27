# ---
# Name: Règle de calcul de la revalorisation standard rente
# Short Name: revalorisation_standard_rente
# Type: benefit_revaluation
# ---

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
# modif du 31/10/2017 date de debut de revalo changé de date_debut_prejudice à date_arret_travail
date_debut_prejudice = date_de_debut_du_prejudice()
# date_arret_travail = date_debut_arret_de_travail()
mode_revalo = param_1_reval_mode_rente()
salaire_annuel_base = salaire_journalier_de_base()
description = description_du_calcul_du_salaire()

frequence_revalo = param_5_frequence_revalo_rente()

if frequence_revalo :
    if '/' not in frequence_revalo:
        frequence_revalo = '01/01/YEARLY'
    jour_synchro, mois_synchro, frequence = frequence_revalo.split('/')

# Calcul des dates pivots
dates = dates_pivot(date_debut_periode, date_fin_periode, frequence, int(mois_synchro), int(jour_synchro))

# calcul des sous périodes
periodes = sous_periodes(dates, date_debut_periode, date_fin_periode)

# calcul du montant pour chaque période
res = []
salaire_reference_revalorise = salaire_annuel_base
initial_description = description
total_amount = 0
details_total_amount = []

for period in periodes:
    periodes_rente = periode_de_rente(period[0], period[1])
    for date_debut, date_fin, periode_entiere, prorata, unit in periodes_rente:
        date_calcul_point = datetime.date(date_debut.year, 1, 1)    
        description = initial_description

        
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
            if code_assureur() == 'PM060':
               mode_revalo = '060_AGIRC_ARRCO'
            if code_assureur() == 'PM056':
               mode_revalo = '056_AGIRC_ARRCO'
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
            taux_revalo = table_AGIRC(date_calcul_point) / table_AGIRC(date_debut_prejudice)
        elif mode_revalo == 'ARRCO':
            taux_revalo = table_ARRCO(date_calcul_point) / table_ARRCO(date_debut_prejudice)
        elif mode_revalo == 'AGIRC_ARRCO':
            taux_revalo = table_AGIRC_ARRCO(date_calcul_point) / table_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '000_AGIRC_ARRCO':
            taux_revalo = table_000_AGIRC_ARRCO(date_calcul_point) / table_000_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '001_AGIRC_ARRCO':
            taux_revalo = table_001_AGIRC_ARRCO(date_calcul_point) / table_001_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '003_AGIRC_ARRCO':
            taux_revalo = table_003_AGIRC_ARRCO(date_calcul_point) / table_003_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '004_AGIRC_ARRCO':
            taux_revalo = table_004_AGIRC_ARRCO(date_calcul_point) / table_004_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '007_AGIRC_ARRCO':
            taux_revalo = table_007_AGIRC_ARRCO(date_calcul_point) / table_007_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '011_AGIRC_ARRCO':
            taux_revalo = table_011_AGIRC_ARRCO(date_calcul_point) / table_011_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '015_AGIRC_ARRCO':
            taux_revalo = table_015_AGIRC_ARRCO(date_calcul_point) / table_015_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '020_AGIRC_ARRCO':
            taux_revalo = table_020_AGIRC_ARRCO(date_calcul_point) / table_020_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '022_AGIRC_ARRCO':
            taux_revalo = table_022_AGIRC_ARRCO(date_calcul_point) / table_022_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '032_AGIRC_ARRCO':
            taux_revalo = table_032_AGIRC_ARRCO(date_calcul_point) / table_032_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '044_AGIRC_ARRCO':
            taux_revalo = table_044_AGIRC_ARRCO(date_calcul_point) / table_044_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '045_AGIRC_ARRCO':
            taux_revalo = table_045_AGIRC_ARRCO(date_calcul_point) / table_045_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '060_AGIRC_ARRCO':
            taux_revalo = table_060_AGIRC_ARRCO(date_calcul_point) / table_060_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '056_AGIRC_ARRCO':
            taux_revalo = table_056_AGIRC_ARRCO(date_calcul_point) / table_060_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '064_AGIRC_ARRCO':
            taux_revalo = table_064_AGIRC_ARRCO(date_calcul_point) / table_064_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '069_AGIRC_ARRCO':
            taux_revalo = table_069_AGIRC_ARRCO(date_calcul_point) / table_069_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '099_AGIRC_ARRCO':
            taux_revalo = table_099_AGIRC_ARRCO(date_calcul_point) / table_099_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '105_AGIRC_ARRCO':
            taux_revalo = table_105_AGIRC_ARRCO(date_calcul_point) / table_105_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '118_AGIRC_ARRCO':
            taux_revalo = table_118_AGIRC_ARRCO(date_calcul_point) / table_118_AGIRC_ARRCO(date_debut_prejudice)
        elif mode_revalo == '022_KN_REVALO':
            taux_revalo = table_022_KN_REVALO(date_calcul_point) / table_022_KN_REVALO(date_debut_prejudice)
        elif mode_revalo == '038_SMI_REVALO':
            taux_revalo = table_038_SMI_REVALO(date_calcul_point) / table_038_SMI_REVALO(date_debut_prejudice)
        elif mode_revalo == '040_UNIP_REVALO':
            taux_revalo = table_040_UNIP_REVALO(date_calcul_point) / table_040_UNIP_REVALO(date_debut_prejudice)
        elif mode_revalo == '043_APICIL_REVALO':
            taux_revalo = table_043_APICIL_REVALO(date_calcul_point) / table_043_APICIL_REVALO(date_debut_prejudice)
        elif mode_revalo == '054_LMG_REVALO':
            taux_revalo = table_054_LMG_REVALO(date_calcul_point) / table_054_LMG_REVALO(date_debut_prejudice)
        elif mode_revalo == '056_GENERALI_REVALO':
            taux_revalo = table_056_GENERALI_REVALO(date_calcul_point) / table_056_GENERALI_REVALO(date_debut_prejudice)
        elif mode_revalo == '056_GENERALI_REVALO_20SAL':
            taux_revalo = table_056_GENERALI_REVALO_20SAL(date_calcul_point) / table_056_GENERALI_REVALO_20SAL(date_debut_prejudice)
        elif mode_revalo == '059_KLESIA_PREV_REVALO':
            taux_revalo = table_059_KLESIA_PREV_REVALO(date_calcul_point) / table_059_KLESIA_PREV_REVALO(date_debut_prejudice)
        elif mode_revalo == '063_CARCEPT_REVALO':
            taux_revalo = table_063_CARCEPT_REVALO(date_calcul_point) / table_063_CARCEPT_REVALO(date_debut_prejudice)
        elif mode_revalo == '065_GROUPAMA_ALSACE_REVALO':
            taux_revalo = table_065_GROUPAMA_ALSACE_REVALO(date_calcul_point) / table_065_GROUPAMA_ALSACE_REVALO(date_debut_prejudice)
        elif mode_revalo == '067_GRESHAM_REVALO':
            taux_revalo = table_067_GRESHAM_REVALO(date_calcul_point) / table_067_GRESHAM_REVALO(date_debut_prejudice)
        elif mode_revalo == '083_IDMUT_REVALO':
            taux_revalo = table_083_IDMUT_REVALO(date_calcul_point) / table_083_IDMUT_REVALO(date_debut_prejudice)
        elif mode_revalo == '085_IDMUT_REVALO':
            taux_revalo = table_085_IDMUT_REVALO(date_calcul_point) / table_085_IDMUT_REVALO(date_debut_prejudice)
        elif mode_revalo == '087_KLESIA_PREV_REVALO':
            taux_revalo = table_087_KLESIA_PREV_REVALO(date_calcul_point) / table_087_KLESIA_PREV_REVALO(date_debut_prejudice)
        elif mode_revalo == '110_SMAVIE_REVALO':
            taux_revalo = table_110_SMAVIE_REVALO(date_calcul_point) / table_110_SMAVIE_REVALO(date_debut_prejudice)
        elif mode_revalo == '117_ARPEGE_REVALO':
            taux_revalo = table_117_ARPEGE_REVALO(date_calcul_point) / table_117_ARPEGE_REVALO(date_debut_prejudice)
        
        ### SPECIFIQUE PARTENAIRE FIN
        

        salaire_annuel_revalorise = arrondir(salaire_annuel_base * taux_revalo, 0.01)
        salaire_reference_revalorise = salaire_annuel_revalorise * prorata
        total_amount += (prorata * salaire_reference_revalorise)
        if arrondir((salaire_annuel_revalorise - salaire_annuel_base), 0.01) > 0.0:
#            description += 'Date d'arrêt de travail: %s€\n' % (date_debut_prejudice)
#            description += 'taux de la revalorisation: %s€\n' % (taux_revalo)
            description += 'Montant de la revalorisation: %s€\n' % arrondir((salaire_annuel_revalorise - salaire_annuel_base), 0.01)     
            details_total_amount.append('(%s€ * %s)' % (salaire_reference_revalorise, prorata))          
            description += 'Montant total: %s (%s)\n' % (total_amount, ' + '.join(details_total_amount))
        res.append({
                    'start_date': date_debut,
                    'end_date': date_fin,
                    'nb_of_unit': prorata,
                    'unit': unit,
                    'amount': salaire_reference_revalorise,
                    'base_amount': arrondir(salaire_annuel_base, 0.01),
                    'amount_per_unit': salaire_annuel_revalorise,
                    'description': description,
                    'date_limite': None,                            
                    })
    
return res
