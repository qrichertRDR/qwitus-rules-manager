# ---
# Name: Test (sauvegarde recette24_2022_08_11)
# Short Name: test
# Type: benefit
# ---

# ---------------------------------------------
# Initialisation
# ---------------------------------------------
dp = date_debut_periode_indemnisation()
fp = date_fin_periode_indemnisation()
nbj_p = (fp - dp).days + 1

# STRUCTURE RESULTAT
test_p = {
    'reference_j': Decimal(0),
    'contractuel_j': Decimal(0),
    'indemnite_base_j': Decimal(0),
    'prestation_j': Decimal(0),
    'prestation_rv_j': Decimal(0)
}

description = ''
res_p = {
    'start_date': dp,
    'end_date': fp,
    'nb_of_unit': nbj_p,
    'unit':
        'day',
    'amount': Decimal(0),
    'base_amount': Decimal(0),
    'amount_per_unit': Decimal(0),
    'description': description,
    'extra_details': {
    },
    'test_data': test_p
}

res = [res_p]

startD=datetime.date(2010, 1, 1)
endD=date_de_debut_du_prejudice()
nbjFrCumul = nb_jour_franchise(startD, endD)
message_debug(nbjFrCumul)

message_debug(periodes_indemnisation_calculees())

return res
