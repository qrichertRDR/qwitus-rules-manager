# ---
# Name: Eligibilité prestation
# Short Name: coog_eligibite_prestation
# Type: benefit
# ---

if service_deductible():
    ajouter_info(u'La prestation est dans la période de franchise cumulée')
    return True

# gestion du délai de déclaration
date_declaration = date_declaration_sinistre()
fin_franchise = date_fin_franchise() or date_de_debut_du_prejudice()
date_debut_prejudice = date_de_debut_du_prejudice()
definition = param_2_delai_de_declaration_definition()
delai = param_1_delai_de_declaration_quantite()
date_max_declaration = ajouter_jours(date_debut_prejudice, 1)
delai_max_rechute = param_3_periode_maximale_entre_un_precedent_arret_et_une_rechute_quantite()
delai_max_rechute_periodicite = param_4_periode_maximale_entre_un_precedent_arret_et_une_rechute_type_periodicite()

if definition == 'jour_apres_arret_travail':
    date_max_declaration = ajouter_jours(date_debut_prejudice, delai)
elif definition == 'mois_apres_arret_travail':
    date_max_declaration = ajouter_mois(date_debut_prejudice, delai)
elif definition == 'jour_apres_franchise':
    date_max_declaration = ajouter_jours(fin_franchise, delai)
elif definition == 'mois_apres_franchise':
    date_max_declaration = ajouter_mois(fin_franchise, delai)
if date_max_declaration < date_declaration:
    if 'accord_de_prise_en_charge' not in documents_recus():
        ajouter_info(u'La date de déclaration saisie %s est superieure à la date maximale de déclaration %s. '
            u'Un accord de prise en charge est nécessaire pour continuer.' % (
                formater_date(date_declaration), formater_date(date_max_declaration)))
        return False

# gestion du délai de rechute
if est_une_rechute():
    date_max_rechute = date_fin_dernier_prejudice()
    if delai_max_rechute_periodicite == 'mois':
        date_max_rechute = ajouter_mois(date_max_rechute, delai_max_rechute)
    else:
        date_max_rechute = ajouter_jours(date_max_rechute, delai_max_rechute)
    if date_de_debut_du_prejudice() > date_max_rechute:
        if 'accord_de_prise_en_charge' not in documents_recus():
            ajouter_info(u'Pour une rechute, le nouvel arret doit survenir avant le %s.'
                u'Un accord de prise en charge est nécessaire pour continuer'
                u' ou vous pouvez créer un nouveau dossier de prestations' % formater_date(date_max_rechute))
            return False

return True
