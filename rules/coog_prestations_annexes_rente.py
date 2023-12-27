# ---
# Name: Prestations annexes rente
# Short Name: coog_prestations_annexes_rente
# Type: tool
# ---

rente_de_base = param_rente_de_base()
salaire_de_reference = param_salaire_de_reference()

date_debut_periode = param_date_debut_periode()
date_fin_periode = param_date_fin_periode()
description = u''
rente_ss = param_rente_ss()
rente_de_base = param_rente_de_base() - rente_ss 
description += 'Déduction de la rente SS: %s - %s = %s\n' % (param_rente_de_base(), rente_ss, rente_de_base)

# Déduction des prestations annexes si applicable
montant_prestations_annexes = montant_de_deduction(None, date_debut_periode, date_fin_periode)
if montant_prestations_annexes:
    montant_prestations_annexes = arrondir(montant_prestations_annexes * jours_entre(date_debut_periode,
        date_fin_periode), 0.01)
    limite = salaire_de_reference - montant_prestations_annexes - rente_ss
    description += u'Calcul de la limite en cas de prestations annexes (%s)\n' % montant_prestations_annexes 
    description += 'Limite = %s\n' % limite
    if rente_de_base > limite:
        # On verifie que la limite est positive sinon elle est egale a 0, donc elle ne peux pas etre strictement negative.
        limite = max(limite, Decimal(0))
        # On limite rente_de_base a la la valeur de la limite.
        rente_de_base = min(rente_de_base, limite)
        description += u'Application de la limite : la nouvelle rente de base est %s\n' % rente_de_base
    else:
        description += u'Limite non depassée: rente de base = %s\n' % rente_de_base

rente_de_base = max(rente_de_base, Decimal('0'))
return rente_de_base, description
