# ---
# Name: Règle de calcul de la revalorisation spécifique
# Short Name: regle_de_calcul_de_la_revalorisation_specifique
# Type: benefit_revaluation
# ---

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
date_debut_prejudice = date_de_debut_du_prejudice()
mode_revalo = param_1_reval_mode_spec()
salaire_journalier_base = salaire_journalier_de_base()
description = description_du_calcul_du_salaire()

frequence_revalo = param_5_frequence_revalo_spec()
if not frequence_revalo or '/' not in frequence_revalo:
    frequence_revalo = '01/01/YEARLY'
jour_synchro, mois_synchro, frequence = frequence_revalo.split('/')

# Calcul des dates pivots
dates = dates_pivot(date_debut_periode, date_fin_periode, frequence, int(mois_synchro), int(jour_synchro))

# calcul des sous périodes
periodes = sous_periodes(dates, date_debut_periode, date_fin_periode)

# calcul du montant pour chaque période
res = []
salaire_journalier_revalorise = salaire_journalier_base
initial_description = description
for period in periodes:     
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
