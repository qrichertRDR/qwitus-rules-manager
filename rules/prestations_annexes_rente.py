# ---
# Name: Prestations annexes rente
# Short Name: prestations_annexes_rente
# Type: tool
# ---

# Cette règle calcule le montant de la rente de base en cas de prestations annexes
type_de_regle = param_type_de_regle()
description = '\n'
rente_de_base = param_rente_de_base()
rente_ss = param_rente_SS()
rente_ss_rellement_percue = param_rente_ss_reellement_percue()
if rente_ss_rellement_percue is None:
    rente_ss_rellement_percue = 0
if limite_au_net():
    libelle_salaire = 'Salaire de référence net'
    salaire_de_reference = param_salaire_de_reference_net()
else:
    if param_salaire_de_reference() == param_salaire_de_reference_net():
       libelle_salaire = 'Salaire de référence net'
    else:
       libelle_salaire = 'Salaire de référence brut'
    salaire_de_reference = param_salaire_de_reference()

# Prestations pôle emploi
prestation_pole_emploi_journalier = montant_de_deduction('pole_emploi', param_date_debut_periode(), param_date_fin_periode())
if prestation_pole_emploi_journalier:
    prestation_pole_emploi = arrondir(prestation_pole_emploi_journalier * ((param_date_fin_periode() - param_date_debut_periode()).days + 1), 0.01)
    limite = salaire_de_reference -rente_ss_rellement_percue - prestation_pole_emploi
    description += 'Calcul de la limite en cas de versement pôle emploi\n'
    description += '%s - rente de la sécurité sociale - versement pôle emploi\n' % libelle_salaire
    description += '%s€ - %s€ - %s€ = %s€\n' % (salaire_de_reference, rente_ss_rellement_percue, prestation_pole_emploi, limite)
    if rente_de_base > limite:
        if limite < 0:
            limite = 0
        rente_de_base = limite
        description += 'Application de la limite: la nouvelle rente de base est %s€\n' % rente_de_base
    else:
        description += 'Le cumul des prestations étant supérieur au salaire de référence, notre rente complémentaire est limitée à notre rente de base soit : %s€.' % rente_de_base
    return rente_de_base, description

# Prestations temps partiel    
if type_de_regle == 'taux_activite':
    taux_activite = compl_taux_d_activite_mi_temps_therapeuthique() / 100
    if not taux_activite:
        return rente_de_base, description
    salaire_mi_temps = ((taux_activite or 0) * salaire_de_reference)
    salaire_mi_temps = arrondir(salaire_mi_temps, 0.01)
    limite = salaire_de_reference - rente_ss - salaire_mi_temps
    description += 'Calcul de la limite en cas de temps partiel\n'
    description += '%s - rente de la sécurité sociale - (taux d''activité * salaire de référence)\n' % libelle_salaire
    description += '%s€ - %s€ - (%s * %s€) = %s€\n' % (salaire_de_reference, rente_ss, taux_activite, salaire_de_reference, limite)
    if rente_de_base > limite:
        #Modification Limite 31/10/2017 - CRU/GGA
        #On vérifie que la limite est positive sinon elle est égale à 0, donc elle ne peux pas etre strictement négative.
        limite = max(limite,0)
        #On limite rente_de_base à la la valeur de la limite.
        rente_de_base = min(rente_de_base, limite)
        description += 'Application de la limite : la nouvelle rente de base est %s€\n' % rente_de_base
    else:
        description += 'Le cumul des prestations étant supérieur au salaire de référence, notre rente complémentaire est limitée à notre rente de base soit : %s€.' % rente_de_base
   
elif type_de_regle == 'ancienne_regle_allianz':
    salaire_temps_partiel_journalier = montant_de_deduction('part_time', param_date_debut_periode(), param_date_fin_periode())
    if not salaire_temps_partiel_journalier:
        return rente_de_base, description
    salaire_temps_partiel = arrondir(salaire_temps_partiel_journalier * ((param_date_fin_periode() - param_date_debut_periode()).days + 1), 0.01)
    message_debug(salaire_de_reference)
    message_debug(rente_ss_rellement_percue)
    message_debug(salaire_temps_partiel)
    limite =salaire_de_reference - rente_ss_rellement_percue - salaire_temps_partiel
    description += 'Calcul de la limite en cas de temps partiel\n'
    description += '%s - rente de la sécurité sociale - salaire temps partiel perçu\n' % libelle_salaire
    description += '%s€ - %s€ - %s€ = %s€\n' % (salaire_de_reference, rente_ss_rellement_percue, salaire_temps_partiel, limite)
    if rente_de_base > limite:
        if limite < 0:
            limite = 0
        rente_de_base = limite
        description += 'Application de la limite: la nouvelle rente de base est %s€\n' % rente_de_base
    else:
        description += 'Le cumul des prestations étant supérieur au salaire de référence, notre rente complémentaire est limitée à notre rente de base soit : %s€.' % rente_de_base
        
return rente_de_base, description
