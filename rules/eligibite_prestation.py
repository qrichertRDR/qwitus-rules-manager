# ---
# Name: Eligibite prestation
# Short Name: eligibite_prestation
# Type: benefit
# ---

if service_deductible():
    ajouter_info(u'La prestation est dans la période de franchise cumulée')
    return True

# gestion du délai de déclaration
date_declaration = date_declaration_sinistre()
fin_franchise = date_fin_franchise() or date_de_debut_du_prejudice()
date_debut_prejudice = date_de_debut_du_prejudice()
definition = compl_delai_de_declaration_definition()
date_max_declaration = ajouter_jours(date_debut_prejudice, 1)

if definition == 'jour_apres_arret_travail':
    date_max_declaration = ajouter_jours(date_debut_prejudice, compl_delai_de_declaration_quantite())
elif definition == 'mois_apres_arret_travail':
    date_max_declaration = ajouter_mois(date_debut_prejudice, compl_delai_de_declaration_quantite())
elif definition == 'jour_apres_franchise':
    date_max_declaration = ajouter_jours(fin_franchise, compl_delai_de_declaration_quantite())
elif definition == 'mois_apres_franchise':
    date_max_declaration = ajouter_mois(fin_franchise, compl_delai_de_declaration_quantite())
if date_max_declaration < date_declaration:
    if 'accord_de_prise_en_charge' not in documents_recus():
        ajouter_info(u'La date de déclaration saisie %s est superieure à la date maximale de déclaration %s. '
            u'Un accord de prise en charge est nécessaire pour continuer.' % (
                formater_date(date_declaration), formater_date(date_max_declaration)))
        return False

# gestion du délai de rechute
if est_une_rechute():
    date_max_rechute = date_fin_dernier_prejudice()
    if compl_periode_maximale_entre_un_precedent_arret_et_une_rechute_type_periodicite() == 'mois':
        date_max_rechute = ajouter_mois(date_max_rechute, compl_periode_maximale_entre_un_precedent_arret_et_une_rechute_quantite())
    else:
        date_max_rechute = ajouter_jours(date_max_rechute, compl_periode_maximale_entre_un_precedent_arret_et_une_rechute_quantite())
    if date_de_debut_du_prejudice() > date_max_rechute:
        if 'accord_de_prise_en_charge' not in documents_recus():
            ajouter_info(u'Pour une rechute, le nouvel arret doit survenir avant le %s.'
                u'Un accord de prise en charge est nécessaire pour continuer'
                u' ou vous pouvez créer un nouveau dossier de prestations' % formater_date(date_max_rechute))
            return False
            
return True
