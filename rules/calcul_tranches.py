# ---
# Name: Calcul tranches
# Short Name: calcul_tranches
# Type: benefit
# ---

description = param_description()
tauxTA = param_tauxTA()
tauxTB = param_tauxTB()
tauxTC = param_tauxTC()
ta = param_ta()
tb = param_tb()
tc = param_tc()

salaire_de_reference = param_salaire_de_reference()
rente_SS = param_rente_ss()
rente_de_base = param_rente_de_base()

trancheTA, trancheTB, trancheTC = 0, 0, 0
if tauxTA:
    trancheTA = arrondir(tauxTA * ta / 100.0, 0.01)
    salaire_de_reference += ta
    rente_de_base += trancheTA
    description += u'Salaire de base (TA): %s * %s = %s\n' % (tauxTA, ta, trancheTA)
if tauxTB:
    trancheTB = arrondir(tauxTB * tb / 100.0, 0.01)
    salaire_de_reference += tb
    rente_de_base += trancheTB
    description += u'Salaire de base (TB): %s * %s = %s\n' % (tauxTB, tb, trancheTB)
if tauxTC:
    trancheTC = arrondir(tauxTC * tc / 100.0, 0.01)
    salaire_de_reference += tc
    rente_de_base += trancheTC
    description += u'Salaire de base (TC): %s * %s = %s\n' % (tauxTC, tc, trancheTC)

salaire_de_reference = arrondir(salaire_de_reference, 0.01)
rente_de_base = arrondir(rente_de_base, 0.01)


description += u'Rente Securite Sociale pour la période: %s\n' % rente_SS

return [{
    'trancheTA': trancheTA,
    'trancheTB': trancheTB,
    'trancheTC': trancheTC,
    'salaire_de_reference': salaire_de_reference,
    'rente_de_base': rente_de_base,
    'description': description
    }]
