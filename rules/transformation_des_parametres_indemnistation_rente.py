# ---
# Name: Transformation des paramètres indemnistation par enfant a charge rente
# Short Name: transformation_des_parametres_indemnistation_rente
# Type: tool
# ---

# REGLE pour le FORMAT:
# "enf_min / enf_max: TA, TB, TC | enf_min / enf_max: TA, TB, TC | ...

donnee = param_donnee()
taux_par_enfant = {}
donnee = donnee.replace('-', '/')
for definition in donnee.split('|'):
    definition = definition.strip()
    enf_min, enf_max = definition.split(':')[0].split('/')
    enf_min = 0 if int(enf_min) >= 99 else int(enf_min)
    ta, tb, tc = definition.split(':')[1].split(',')
    taux_par_enfant[int(enf_min), int(enf_max)] = (Decimal(ta), Decimal(tb), Decimal(tc))
return taux_par_enfant
