# ---
# Name: Régularisation eckert
# Short Name: revalorisation_eckert
# Type: benefit_revaluation
# ---

date_deces = date_debut_periode_indemnisation()
date_paiement = date_fin_periode_indemnisation()
capital_de_base = salaire_journalier_de_base()
description = description_du_calcul_du_salaire()
description += '\n'

# calcul de la date de premiere revalo
if not compl_montant_de_revalorisation_eckert():
    if date_paiement.year == date_deces.year:
        nb_jour_annee = (datetime.date(date_paiement.year, 12, 31) - datetime.date(date_paiement.year, 1, 1)).days
        taux = (1 + table_taux_de_revalorisation_eckert(date_paiement)) ** (1.0 * ((date_paiement - date_deces).days) / nb_jour_annee) * 1.0
    elif date_paiement.year - date_deces.year >= 1:
        nb_jour_annee_paiement = (datetime.date(date_paiement.year, 12, 31) - datetime.date(date_paiement.year, 1, 1)).days
        nb_jour_annee_deces = (datetime.date(date_deces.year, 12, 31) - datetime.date(date_deces.year, 1, 1)).days
        nb_jour_paiement = (date_paiement - datetime.date(date_paiement.year, 1, 1)).days
        nb_jour_deces = (datetime.date(date_deces.year, 12, 31) - date_deces).days
        taux = ((1 + table_taux_de_revalorisation_eckert(date_paiement)) ** (1.0 * nb_jour_paiement / nb_jour_annee_paiement)) * \
                ((1 + table_taux_de_revalorisation_eckert(date_deces)) ** (1.0 * nb_jour_deces / nb_jour_annee_deces))
        if (date_paiement.year - date_deces.year) >= 2:
            for y in range(date_deces.year + 1, date_paiement.year):
                taux = taux * (1 + table_taux_de_revalorisation_eckert(datetime.date(y, 1, 1)))
    description += 'Taux de revalorisation Eckert : %s\n' % str(taux)
    capital_revalorise = taux * capital_de_base
else:
    capital_revalorise = capital_de_base + compl_montant_de_revalorisation_eckert()

capital_revalorise = arrondir(capital_revalorise, 0.01)
extra_data = {'revalorisation_eckert': capital_revalorise - capital_de_base, 'montant_capital_base': capital_de_base}
description += 'Montant de la revalorisation : %s€\n' % str(extra_data['revalorisation_eckert'])
description += 'Montant du capital revalorisé : %s€\n' % str(capital_revalorise)

# calcul de la pénalité
total = capital_revalorise
if not compl_montant_des_penalites_eckert():
    description += '\n\nCalcul des pénalités\n'
    fin = date_fin_periode_indemnisation()
    docs = reception_des_documents_beneficiaire()
    message_debug(docs)
    debut_majo_1 = ajouter_mois(docs, 1)
    message_debug(debut_majo_1)
    debut_majo_2 = ajouter_mois(debut_majo_1, 2)
    message_debug(debut_majo_2)
    message_debug(fin)

    # Ajout de 6 mois pour détecter un changement de plus
    dates = dates_changement_table('taux_penalite_eckert', 1,
        debut_majo_1, ajouter_mois(fin, 6))
    if fin > debut_majo_1:
        dates.append(debut_majo_1)
    if fin > debut_majo_2:
        dates.append(debut_majo_2)
    dates.append(fin)
    dates.sort()
    message_debug(dates)
    penalite = 0
    for idx, base_date in enumerate(dates[:-1]):
        period_start = base_date
        period_end = ajouter_jours(dates[idx + 1], -1)
        description += 'Periode du %s au %s\n' % (str(period_start), str(period_end))
        
        # Calcul du taux
        taux = table_taux_penalite_eckert(period_start)
        description += '    Taux de base : %.2f%%\n' % taux
        if period_start >= debut_majo_2:
            taux *= 3
            description += '    Taux appliqué : %.2f%% \n' % taux
        elif period_start >= debut_majo_1:
            taux *= 2
            description += '    Taux appliqué : %.2f%% \n' % taux
        taux = taux / 100
        
        # Nombre de jours pour le prorata
        base = (ajouter_annees(period_start, 1, True) - period_start).days
        delta = (period_end - period_start).days - 1
        description += '    Nombre de jours sur la période : %s \n' % str(delta)
        description += "    Nombre de jours de l'année correspondante : %s \n" % str(base)
        
        montant = arrondir(capital_revalorise * taux * delta / base, 0.01)
        penalite += montant
        total += montant
        description += '    Pénalités : %s€\n\n' % str(montant)
        
else:
    penalite = compl_montant_des_penalites_eckert()
    total += penalite
    
description += 'Montant total des pénalités : %.2f€\n' % penalite 
description += 'Montant du capital total : %.2f€\n' % total
extra_data['penalites_eckert'] = penalite
return [{
        'start_date': date_deces,
        'end_date': date_paiement,
        'nb_of_unit': 1,
        'unit': 'day',
        'amount': total,
        'amount_per_unit': total,
        'base_amount': capital_de_base,
        'description': description,
        'extra_details': extra_data,
        }]
