# ---
# Name: Transformation des paramètres indemnistation par enfant a charge et périodes
# Short Name: parsing_ij_child_and_period
# Type: tool
# ---

# REGLE pour le FORMAT:
# "palier - enf_min / enf_max: TA, TB, TC, TA_palier, TB_palier, TC_palier | palier - enf_min / enf_max: TA, TB, TC ... | ...
 
donnees = param_data()
donnees_par_enfants = {}
for donnee in donnees.split('|'):
    palier = donnee.split('-')[0].strip()
    palier = int(palier)
    definition = donnee.split('-')[1].strip()
    enf_min, enf_max = definition.split(':')[0].split('/')
    enf_min = 0 if int(enf_min) >= 99 else int(enf_min)
    enf_max = int(enf_max)
    tranche_enfant = (enf_min, enf_max)
    TA, TB, TC, TA_palier, TB_palier, TC_palier = definition.split(':')[1].split(',')
    if tranche_enfant not in donnees_par_enfants:
        donnees_par_enfants[tranche_enfant] = {}    
    donnees_par_enfants[tranche_enfant][palier] = (Decimal(TA), Decimal(TB), Decimal(TC), 
        Decimal(TA_palier), Decimal(TB_palier), Decimal(TC_palier))

return donnees_par_enfants
