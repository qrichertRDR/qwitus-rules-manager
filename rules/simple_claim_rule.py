# ---
# Name: Simple Claim Rule
# Short Name: simple_claim_rule
# Type: benefit
# ---

date_debut = date_debut_periode_indemnisation()
date_fin = date_fin_periode_indemnisation()
if date_debut and date_fin:
    return [{
        'start_date': date_debut,
        'end_date': date_fin,
        'nb_of_unit': (date_fin - date_debut).days + 1,
        'unit': 'day',
        'amount': ((date_fin - date_debut).days + 1) * param_claim_amount(),
        'amount_per_unit': param_claim_amount()
        }]
else:
    return [{
        'start_date': date_debut,
        'end_date': date_fin,
        'nb_of_unit': 1,
        'unit': 'day',
        'amount': param_claim_amount(),
        'amount_per_unit': param_claim_amount()
        }]
