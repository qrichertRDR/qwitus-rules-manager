# ---
# Name: Salaire brut par tranche de salaire avec palier et enfant
# Short Name: SB_palier_enfant
# Type: benefit
# ---

# Pas d'indémnisation si IJSS nulle
IJSS = compl_ijss()
donnee_a_transformer = param_1_donnees()
donnees_transformees = rule_parsing_ij_child_and_period(data=donnee_a_transformer)
nbr_enfants = compl_nombre_d_enfants_a_charge()
date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
res = []
tranches = tranche_salaire(['gross_salary',  'salary_bonus'])
donnees = None
for tranche_enfant, value in donnees_transformees.items():
    enf_min, enf_max = tranche_enfant
    if nbr_enfants >= enf_min or nbr_enfants <= enf_max:
        donnees = value
        break
if not donnees:
    ajouter_erreur(u"Le paramétrage du contrat collectif n'indique pas les périodes pour %s enfant(s)" % nbr_enfants)


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

# potentiellement plusieurs paliers, mais pas pour le moment:
palier = donnees.keys()[0]
          
ta, tb, tc, ta_reduit, tb_reduit, tc_reduit = donnees[palier]

# Besoin de découper la période si il y a un palier et que le palier traverse cette période.
if ajouter_jours(date_debut_periode, palier) < date_fin_periode:
    sub_periods = [(date_debut_periode, ajouter_jours(date_debut_periode, palier)), 
        (ajouter_jours(date_debut_periode, palier + 1), date_fin_periode)]
else:
    sub_periods = [(date_debut_periode, date_fin_periode)]

# Calcul pour chaque sous période (potentiellement deux sous période si palier défini)
for sous_date_debut_periode, sous_date_fin_periode in sub_periods:
    # calcul du montant journalier de base
    description = ''
    salaire_de_base = 0
    if palier and sous_date_fin_periode == date_fin_periode:
        pourcentage_TA = ta_reduit
        pourcentage_TB = tb_reduit
        pourcentage_TC = tc_reduit
    else:
        pourcentage_TA = ta
        pourcentage_TB = tb
        pourcentage_TC = tc
        
    if pourcentage_TA:
        trancheTA = arrondir(pourcentage_TA * tranches['TA'] / 100.0, 0.01)
        salaire_de_base += trancheTA
        description += 'Salaire de référence (TA): %s * %s€ /100 = %s€\n' % (pourcentage_TA, tranches['TA'], trancheTA)
    if pourcentage_TB:
        trancheTB = arrondir(pourcentage_TB * tranches['TB'] / 100.0, 0.01)
        salaire_de_base += trancheTB
        description += 'Salaire de référence (TB): %s * %s€ /100 = %s€\n' % (pourcentage_TB, tranches['TB'], trancheTB)
    if pourcentage_TC:
        trancheTC = arrondir(pourcentage_TC * tranches['TC'] / 100.0, 0.01)
        salaire_de_base += trancheTC
        description += 'Salaire de référence (TC): %s * %s€ /100 = %s€\n' % (pourcentage_TC, tranches['TC'], trancheTC)
    description += 'Salaire de référence: %s€\n' % salaire_de_base
    salaire_journalier = arrondir(salaire_de_base / 365, 0.01)
    description += 'Salaire de référence journalier: %s€ / 365 = %s€\n\n' % (salaire_de_base, salaire_journalier)

    # mi temps therapeutique
    montant_mi_temps = arrondir(montant_de_deduction('mi-temps_therapeutique', sous_date_debut_periode, sous_date_fin_periode), 0.01)
    salaire_reduit_moitie = False
    if montant_mi_temps:
        montant_mi_temps_total = arrondir(montant_mi_temps * ((sous_date_fin_periode - sous_date_debut_periode).days + 1), 0.01)
        salaire_journalier = arrondir(salaire_journalier / 2, 0.01)
        description += 'Versement employeur - Mi temps thérapeutique: %s€ (montant journalier: %s€)\n\n' % (montant_mi_temps_total, montant_mi_temps)
        salaire_reduit_moitie = True

    # IJSS
    IJSS_total = IJSS * ((sous_date_fin_periode - sous_date_debut_periode).days + 1)
    description += 'Versement sécurité sociale: %s€ (IJSS: %s€)\n\n' % (IJSS_total, IJSS)

    # Limiter à 100% du salaire de base
    if salaire_reduit_moitie:
        description += 'Salaire journalier réduit de moitié: %s€\n' % salaire_journalier
    salaire_reference = tranches['TA'] + tranches['TB'] + tranches['TC']
    limite = arrondir(salaire_reference / 365, 0.01)
    if (trancheTA and limite <= salaire_journalier + montant_mi_temps) or (not trancheTA and salaire_journalier + IJSS + montant_mi_temps):
        salaire_journalier_base = arrondir((tranches['TA'] + tranches['TB'] + tranches['TC']) / 365, 0.01) - IJSS - montant_mi_temps
        description += 'Limitation à 100 pourcent du salaire soit %s€\n\n' % max(salaire_journalier_base, 0)
    else:
        salaire_journalier_base = salaire_journalier - IJSS
        description += "Salaire de base journalier déduit de l'IJSS: %s€ - %s€ = %s€\n\n" % (salaire_journalier, IJSS, salaire_journalier_base)
    if salaire_journalier_base < 0:
        salaire_journalier_base = 0

    if compl_ij_de_base_corrige():
        salaire_journalier_base = compl_ij_de_base_corrige() 
        description = 'Salaire de base journalier: %s€\n' % salaire_journalier_base

    res.append({
            'start_date': sous_date_debut_periode,
            'end_date': sous_date_fin_periode,
            'nb_of_unit': (sous_date_fin_periode - sous_date_debut_periode).days + 1,
            'unit': 'day',
            'amount': salaire_journalier_base * ((sous_date_fin_periode - sous_date_debut_periode).days + 1),
            'base_amount': salaire_journalier_base,
            'amount_per_unit': salaire_journalier_base,
            'description': description,
            'limit_date': None,
            'extra_details': {
                'tranche_a': trancheTA,
                'tranche_b': trancheTB, 
                'tranche_c': trancheTC,
                'ijss': str(IJSS),
                'sanction_ijss': str(compl_sanction_ijss()),
                }
            })
return res
