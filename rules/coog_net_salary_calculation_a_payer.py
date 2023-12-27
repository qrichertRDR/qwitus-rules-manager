# ---
# Name: Calcul du salaire NET (A payer)
# Short Name: coog_net_salary_calculation_a_payer
# Type: benefit_net_salary_calculation
# ---

tranches = tranche_salaire(['gross_salary', 'salary_bonus'], with_revaluation=False)
TRA = tranches['TA']
TRB = tranches['TB']
TRC = tranches['TC']

#calcul des contributions salariales
contrib_salariales = ['4_coog_chomage_1', '4_coog_chomage_2',
    '3_coog_prevoyance_1', '3_coog_prevoyance_2', '2_coog_retraite_1', '2_coog_retraite_2',
    '1_coog_urssaf_1', '1_coog_urssaf_2', '1_coog_urssaf_3', '1_coog_urssaf_4',
    '6_coog_charges_salariales_sante_taux']
TA = taux_de_la_tranche('A', fixed=False, codes_list=contrib_salariales) or 0.0
TB = taux_de_la_tranche('B', fixed=False, codes_list=contrib_salariales) or 0.0
TC = taux_de_la_tranche('C', fixed=False, codes_list=contrib_salariales) or 0.0

total_salaire_net = (TRA * (1 - TA / 100.0)
    + TRB * (1 - TB / 100.0)
    + TRC * (1 - TC / 100.0))

#calcul de la CSG/RDS
contrib_patronales = ['5_coog_charges_patronales_prevoyance', '6_coog_charges_patronales_sante_taux']
assiette_csg_rds = 0.9825 * (TRA + TRB + TRC) \
    + taux_de_la_tranche('A', fixed=False, codes_list=contrib_patronales) * TRA / 100.0 \
    + taux_de_la_tranche('B', fixed=False, codes_list=contrib_patronales) * TRB / 100.0 \
    + taux_de_la_tranche('C', fixed=False, codes_list=contrib_patronales) * TRC / 100.0
assiette_csg_rds += taux_de_la_tranche(fixed=True, codes_list=['2_coog_charges_patronales_sante_montant'])
total_salaire_net -= assiette_csg_rds * (0.005 + 0.051 + 0.024)

#Enlever le montant de la prévoyance
total_salaire_net -= taux_de_la_tranche(fixed=True, codes_list=['1_coog_charges_salariales_mutuelle'])

tranches = tranche_salaire(['gross_salary'], with_revaluation=False)
TRA = tranches['TA']
TRB = tranches['TB']
TRC = tranches['TC']

#calcul des contributions salariales
contrib_salariales = ['4_coog_chomage_1', '4_coog_chomage_2',
    '3_coog_prevoyance_1', '3_coog_prevoyance_2', '2_coog_retraite_1', '2_coog_retraite_2',
    '1_coog_urssaf_1', '1_coog_urssaf_2', '1_coog_urssaf_3', '1_coog_urssaf_4',
    '6_coog_charges_salariales_sante_taux']
TA = taux_de_la_tranche('A', fixed=False, codes_list=contrib_salariales) or 0.0
TB = taux_de_la_tranche('B', fixed=False, codes_list=contrib_salariales) or 0.0
TC = taux_de_la_tranche('C', fixed=False, codes_list=contrib_salariales) or 0.0

salaire_net = (TRA * (1 - TA / 100.0)
    + TRB * (1 - TB / 100.0)
    + TRC * (1 - TC / 100.0))

#calcul de la CSG/RDS
contrib_patronales = ['5_coog_charges_patronales_prevoyance', '6_coog_charges_patronales_sante_taux']
assiette_csg_rds = 0.9825 * (TRA + TRB + TRC) \
    + taux_de_la_tranche('A', fixed=False, codes_list=contrib_patronales) * TRA / 100.0 \
    + taux_de_la_tranche('B', fixed=False, codes_list=contrib_patronales) * TRB / 100.0 \
    + taux_de_la_tranche('C', fixed=False, codes_list=contrib_patronales) * TRC / 100.0
assiette_csg_rds += taux_de_la_tranche(fixed=True, codes_list=['2_coog_charges_patronales_sante_montant'])
salaire_net -= assiette_csg_rds * (0.005 + 0.051 + 0.024)

#Enlever le montant de la prévoyance
salaire_net -= taux_de_la_tranche(fixed=True, codes_list=['1_coog_charges_salariales_mutuelle'])

return arrondir(salaire_net, 0.01), arrondir(total_salaire_net - salaire_net, 0.01)
