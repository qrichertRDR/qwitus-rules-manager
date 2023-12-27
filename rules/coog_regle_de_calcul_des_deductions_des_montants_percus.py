# ---
# Name: Règle de calcul des déductions des montants percus
# Short Name: coog_regle_de_calcul_des_deductions_des_montants_percus
# Type: benefit
# ---

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
description = ''
traitement_journalier_base_originel = param_traitement_de_base_journalier()
IJSS = abs(param_ijss())
IJSS_deduite = not param_sans_deduction_de_l_ijss()
traitement_de_reference = param_traitement_de_reference()

traitement_journalier_base = traitement_journalier_base_originel
traitement_reference_journalier = arrondir(traitement_de_reference / 365, 0.01)
montant_mi_temps = montant_de_deduction('part_time', date_debut_periode, date_fin_periode)
# Application de la règle de mi-temps thérapeutique si il y à un montant de mi-temps
if montant_mi_temps:
    montant_mi_temps_total = montant_mi_temps * ((date_fin_periode - date_debut_periode).days + 1)
    montant_mi_temps_total = arrondir(montant_mi_temps_total, 0.001)
    description += 'Versement employeur - Mi temps thérapeutique: %s euros (montant journalier: %s€)\n\n' % (montant_mi_temps_total, montant_mi_temps)
    if param_inclusion_du_mi_temps_therapeutique() == 'ijb_ijss_mtt':
        traitement_journalier_base = traitement_journalier_base_originel - IJSS - montant_mi_temps
        description += 'Limitation du mi-temps thérapeutique (Traitement de référence - IJSS - montant percu en mi-temps): %s€ - %s€ - %s€ = %s€\n' % (
            traitement_journalier_base_originel, IJSS, montant_mi_temps, traitement_journalier_base)
    elif param_inclusion_du_mi_temps_therapeutique() == 'tdrj_ijss_mtt':
        traitement_journalier_base = traitement_reference_journalier - IJSS - montant_mi_temps
        description += 'Limitation du mi-temps thérapeutique (100 %% du traitement journalier de référence - IJSS - montant percu en mi-temps): %s€ - %s€ - %s€ = %s€\n' % (
            traitement_reference_journalier, IJSS, montant_mi_temps, traitement_journalier_base)
    elif param_inclusion_du_mi_temps_therapeutique() == 'min_ijb_2_tdrj_mtt':
        ijb_ijss_mtt = traitement_journalier_base_originel - IJSS - montant_mi_temps
        tdrj_divise_par_deux =  arrondir(traitement_reference_journalier / 2, 0.01)
        traitement_journalier_base = min(ijb_ijss_mtt, tdrj_divise_par_deux)
        if tdrj_divise_par_deux > ijb_ijss_mtt:
            description += 'Limitation du mi-temps thérapeutique (Ij de base - IJSS - montant percu en mi-temps): %s€ - %s€ - %s€ = %s€\n' % (
                traitement_journalier_base_originel, IJSS, montant_mi_temps, traitement_journalier_base)
        else:
            description += 'Limitation du mi-temps thérapeutique (100%% traitement journalier de référence / 2 - IJSS - montant percu en mi-temps): %s€ - %s€ - %s€ = %s€\n' % (
                tdrj_divise_par_deux, IJSS, montant_mi_temps, traitement_journalier_base)
    else:
        ajouter_erreur(u"La règle de mi-temps thérapeutique est inconnue")
else:
    traitement_journalier_base = traitement_journalier_base - (IJSS if IJSS_deduite else 0)
    if IJSS_deduite:
        description += "Traitement de base journalier déduit de l'IJSS: %s€ - %s€ = %s€\n" % (traitement_journalier_base_originel, IJSS, traitement_journalier_base)
    else:
        description += "Traitement de base journalier sans déduction de l'IJSS: %s€\n" % traitement_journalier_base
return traitement_journalier_base, montant_mi_temps, description
