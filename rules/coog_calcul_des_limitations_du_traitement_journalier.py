# ---
# Name: Calcul des limitations du traitement journalier
# Short Name: coog_calcul_des_limitations_du_traitement_journalier
# Type: benefit
# ---

date_debut_periode = date_debut_periode_indemnisation()
date_fin_periode = date_fin_periode_indemnisation()
traitement_de_reference = param_traitement_de_reference()
description = ''
IJSS = abs(param_ijss())
IJSS_deduite = not param_sans_deduction_de_l_ijss()
limiter_au_net = param_limiter_au_net()
montant_mi_temps = param_montant_du_mi_temps_therapeutique()
calcul_du_net = limite_au_net()
traitement_journalier_base = param_traitement_journalier_de_base()

# Limitation au salaire de base    
traitement_de_reference_journalier = arrondir(traitement_de_reference / 365, 0.01)
# Limiter à 100% du salaire de base
if traitement_journalier_base > traitement_de_reference_journalier - (IJSS if IJSS_deduite else 0) - montant_mi_temps:
    traitement_journalier_base = traitement_de_reference_journalier - (IJSS if IJSS_deduite else 0) - montant_mi_temps
    description += 'Limitation à 100 pourcent du salaire soit %s€\n' % max(traitement_journalier_base, 0)

# IJSS
IJSS_total = IJSS * ((date_fin_periode - date_debut_periode).days + 1)
description += 'Versement sécurité sociale: %s€ (IJSS: %s€)\n\n' % (IJSS_total, IJSS)

# Limitation au net
if calcul_du_net and limiter_au_net:
    salaire_net_journalier = arrondir(salaire_net() / 365, 0.01)
    ajouter_info(salaire_net_journalier)
    ajouter_info(traitement_journalier_base)
    if traitement_journalier_base > salaire_net_journalier - (IJSS if IJSS_deduite else 0) - montant_mi_temps:
        traitement_journalier_base = salaire_net_journalier - (IJSS if IJSS_deduite else 0) - montant_mi_temps
        description += 'Limitation à 100 pourcent du salaire net soit %s€\n' % max(traitement_journalier_base, 0)

if traitement_journalier_base < 0:
    traitement_journalier_base = 0

return traitement_journalier_base, description
