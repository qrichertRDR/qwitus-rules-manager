# ---
# Name: Indémnisation basée sur le PMSS
# Short Name: PMSS
# Type: benefit
# ---

# Pas d'indémnisation si IJSS nulle
IJSS = compl_ijss()
date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
if not IJSS:
    description = "Aucune prestation à verser car l'IJSS est nulle\n"
    return ([{
            'start_date': date_debut_periode,
            'end_date': date_fin_periode,
            'nb_of_unit': (date_fin_periode - date_debut_periode).days + 1,
            'unit': 'day',
            'amount': Decimal(0),
            'base_amount': Decimal(0),
            'amount_per_unit': Decimal(0),
            'description': description,
            }])

# calcul du montant journalier de base
description = ''
pmss = table_pmss(date_de_debut_du_prejudice()) * 12
pourcentage_PMSS = param_1_pourcentage_du_pmss()
description += 'Plafond annuel de la sécurité sociale: %s\n' % pmss
salaire_journalier = arrondir(pmss / 365, 0.01)
description += 'Plafond journalier: %s€ / 365 = %s€\n\n' % (pmss, salaire_journalier)
salaire_journalier = pourcentage_PMSS * salaire_journalier / 100

# mi temps therapeutique
montant_mi_temps = arrondir(montant_de_deduction('part_time', date_debut_periode, date_fin_periode), 0.01)
salaire_reduit_moitie = False
if montant_mi_temps:
    montant_mi_temps_total = arrondir(montant_mi_temps * ((date_fin_periode - date_debut_periode).days + 1), 0.01)
    salaire_journalier = arrondir(salaire_journalier / 2, 0.01)
    description += 'Versement employeur - Mi temps thérapeutique: %s€ (montant journalier: %s€)\n\n' % (montant_mi_temps_total, montant_mi_temps)
    salaire_reduit_moitie = True

# IJSS
IJSS_total = IJSS * ((date_fin_periode - date_debut_periode).days + 1)
description += 'Versement sécurité sociale: %s€ (IJSS: %s€)\n\n' % (IJSS_total, IJSS)
salaire_journalier = salaire_journalier - IJSS 

# resultat final
if salaire_reduit_moitie:
    description += 'Salaire journalier réduit de moitié: %s€\n' % salaire_journalier
description += 'IJSS: %s€\n' % IJSS
salaire_avant_deduction = salaire_journalier
description += "Montant de base réduit de l'IJSS: %s€ - %s€ = %s€\n" % (salaire_avant_deduction, IJSS, salaire_journalier)
if salaire_journalier < 0:
    salaire_journalier = 0

return ([{
            'start_date': date_debut_periode,
            'end_date': date_fin_periode,
            'nb_of_unit': (date_fin_periode - date_debut_periode).days + 1,
            'unit': 'day',
            'amount': salaire_journalier * ((date_fin_periode - date_debut_periode).days + 1),
            'base_amount': salaire_journalier,
            'amount_per_unit': salaire_journalier,
            'description': description,
            'limit_date': None,
            'extra_details': {
                'ijss': str(IJSS),
                'sanction_ijss': str(compl_sanction_ijss()),
                }
            }])
