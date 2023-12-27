# ---
# Name: Message alerte analyses medicales
# Short Name: message_alerte_analyses_medicales
# Type: process_check
# ---

if analyses_medicales_non_recues():
    ajouter_avertissement(u'Avez-vous demandé l\'attestation médicale?')
return
