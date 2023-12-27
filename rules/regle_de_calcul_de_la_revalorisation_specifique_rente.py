# ---
# Name: Règle de calcul de la revalorisation spécifique rente
# Short Name: regle_de_calcul_de_la_revalorisation_specifique_rente
# Type: benefit_revaluation
# ---

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
date_debut_prejudice = date_de_debut_du_prejudice()
mode_revalo = param_1_reval_mode_spec_rente()
salaire_annuel_base = salaire_journalier_de_base()
description = description_du_calcul_du_salaire()

frequence_revalo = param_5_frequence_revalo_spec_rente()
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
        date_calcul_point = datetime.date(period[0].year, 1, 1)
        if mode_revalo == 'APGI':
            taux_revalo = table_APGI(date_calcul_point) / table_APGI(date_debut_prejudice)
        elif mode_revalo == 'CCNBE':
            taux_revalo = table_CCNBE(date_calcul_point) / table_CCNBE(date_debut_prejudice)
        elif mode_revalo == 'GAN':
            taux_revalo = table_GAN(date_calcul_point) / table_GAN(date_debut_prejudice)
        elif mode_revalo == 'IM':
            taux_revalo = table_IM(date_calcul_point) / table_IM(date_debut_prejudice)
        elif mode_revalo == 'OREPA':
            taux_revalo = table_OREPA(date_calcul_point) / table_OREPA(date_debut_prejudice)
        elif mode_revalo == 'RAEG':
            taux_revalo = table_RAEG(date_calcul_point) / table_RAEG(date_debut_prejudice)
        elif mode_revalo == 'ROTH':
            taux_revalo = table_ROTH(date_calcul_point) / table_ROTH(date_debut_prejudice)
        elif mode_revalo == 'TBZ':
            taux_revalo = table_TBZ(date_calcul_point) / table_TBZ(date_debut_prejudice)
        elif mode_revalo == 'UNIRS':
            taux_revalo = table_UNIRS(date_calcul_point) / table_UNIRS(date_debut_prejudice)
        salaire_annuel_revalorise = arrondir(salaire_annuel_base * taux_revalo, 0.01)
        salaire_reference_revalorise = salaire_annuel_revalorise * prorata
        total_amount += (prorata * salaire_reference_revalorise)
        if arrondir((salaire_annuel_revalorise - salaire_annuel_base), 0.01) > 0.0:
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
