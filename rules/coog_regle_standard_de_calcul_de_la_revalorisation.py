# ---
# Name: Règle standard de calcul de la revalorisation
# Short Name: coog_regle_standard_de_calcul_de_la_revalorisation
# Type: benefit_revaluation
# ---

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
date_debut_prejudice = date_de_debut_du_prejudice()
mode_revalo = param_1_reval_mode()
salaire_journalier_base = salaire_journalier_de_base()
description = description_du_calcul_du_salaire().decode('utf-8')
date_maximum_revalo = date_revalorisation_maximum()

# calcul de la date de premiere revalo
if param_2_date_de_reference() == 'DAT' or not date_fin_franchise():
    premiere_revalo = date_de_debut_du_prejudice()
else:
    premiere_revalo = ajouter_jours(date_fin_franchise(), 1)

# Gestion d'une eventuelle règle spécifique pour la première revalorisation
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
    dates.extend(dates_pivot(date_debut_periode, min(date_fin_periode, date_maximum_revalo), 'YEARLY', premiere_revalo.month, premiere_revalo.day))
elif frequence_revalo in ('01/01/YEARLY', '01/07/YEARLY'):
    frequence_revalo = '01/01/YEARLY'
    jour_synchro, mois_synchro, frequence = frequence_revalo.split('/')
    dates.extend(dates_pivot(date_debut_periode, date_fin_periode, frequence, int(mois_synchro), int(jour_synchro)))

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
        if mode_revalo == 'AGIRC':
            taux_revalo = table_COOG_AGIRC(min(period[0], date_maximum_revalo)) / table_COOG_AGIRC(date_debut_prejudice)
        elif mode_revalo == 'ARRCO':
            taux_revalo = table_COOG_ARRCO(min(period[0], date_maximum_revalo)) / table_COOG_ARRCO(date_debut_prejudice)

    salaire_journalier_revalorise = arrondir(salaire_journalier_base * taux_revalo, 0.01)
    if (salaire_journalier_revalorise - salaire_journalier_base) != 0.0:
        description += u'Montant de la revalorisation: %s€\n' % (salaire_journalier_revalorise - salaire_journalier_base)
    nb_jour = (period[1] - period[0]).days + 1
    description += u'Montant total: %s€ * %s = %s€' % (salaire_journalier_revalorise, nb_jour,
        nb_jour * salaire_journalier_revalorise)
    res.append({
            'start_date': period[0],
            'end_date': period[1],
            'nb_of_unit': (period[1] - period[0]).days + 1,
            'unit': 'day',
            'amount': arrondir(((period[1] - period[0]).days + 1) * salaire_journalier_revalorise, 0.01),
            'amount_per_unit': arrondir(salaire_journalier_revalorise, 0.01),
            'base_amount': arrondir(salaire_journalier_base, 0.01),
            'description': description.encode('utf-8'),
            'date_limite': None,
            'extra_details': {
                'montant_revalorisation': salaire_journalier_revalorise - salaire_journalier_base,
                }
            })
return res
