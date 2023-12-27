# ---
# Name: Changement compagnie (partage prestation)
# Short Name: cgt_partage_prestation
# Type: tool
# ---

# DEBUT CGT PARTAGE PRESTATION #
################################

def rule_cgt_partage_prestation(debut_periode, base_courante, base_reva_courante):

    desc_cgt = u''
    base_suivante = base_courante
    base_reva_suivante = base_reva_courante

    rep = rule_cgt_gestion_contrat()

    if rep is None:
        return

    regle_entree, regle_sortie, date_entree, date_sortie, exception = rep

    if regle_entree is not None:

        message_entree = u""

        if regle_entree == 'lock_indemnifications':
            base_ass_n = montant_base_ancien_assureur()
            reva_ass_n = revalorisation_ancien_assureur()
            base_reva_ass_n = base_ass_n + reva_ass_n

            delta_base_courante = (base_reva_courante - base_courante)

            desc_nv_atteint = u''
            '''
            desc_nv_atteint += u'\nBase reprise (journalière) %.2f€ : %.2f€ (base courante) - %.2f€ (base précédente)' % (
                base_courante - base_ass_n, base_courante, base_ass_n)
            '''
            desc_nv_atteint += u'\nRevalorisation reprise (journalière) %.2f€ : %.2f€ (reva. courante) - %.2f€ (reva. précédente)' % (
                delta_base_courante - reva_ass_n, delta_base_courante, reva_ass_n)

            base_suivante = base_suivante - base_ass_n
            base_reva_suivante = base_reva_suivante - base_reva_ass_n

            message_entree += u'\nReprise au niveau atteint'
            message_entree += u" à partir du %s" % formater_date(date_entree)
            message_entree += desc_nv_atteint
        elif regle_entree == 'normal_indemnifications':
            base_suivante = 0
            base_reva_suivante = 0

            message_entree += u'\nAucune reprise'
            message_entree += u" à partir du %s" % formater_date(date_entree)
        elif regle_entree == 'stop_indemnifications':
            pass
            # message_entree += u'Reprise totale'

        desc_cgt += message_entree

    if regle_sortie is not None:

        if debut_periode > date_sortie:
            message_sortie = u''
            if regle_sortie == 'lock_indemnifications':
                message_sortie += u"\nMaintien au niveau atteint"
                message_sortie += u" après le %s" % formater_date(date_sortie)
            elif regle_sortie == 'normal_indemnifications':
                pass
                # message_sortie += u"Maintien total"
            elif regle_sortie == 'stop_indemnifications':
                message_sortie += u"\nAucun maintien"
                message_sortie += u" après le %s" % formater_date(date_sortie)
                base_suivante = 0
                base_reva_suivante = 0
            desc_cgt += message_sortie

    return base_suivante, base_reva_suivante, desc_cgt


def partage_prestation():
    ajouter_info(u"RV1")
    deb = param_debut_periode()
    base = param_base_courante()
    base_reva = param_base_reva_courante()
    return rule_cgt_partage_prestation(debut_periode=deb, base_courante=base,
                                       base_reva_courante=base_reva)

return partage_prestation() # DECOMMENTER SOUS COOG

##############################
# FIN CGT PARTAGE PRESTATION #
