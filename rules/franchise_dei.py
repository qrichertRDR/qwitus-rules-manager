# ---
# Name: Franchise à partir d'une DEI
# Short Name: franchise_dei
# Type: benefit_deductible
# ---

return ajouter_jours(compl_date_de_d_effet_d_indemnisation() or date_de_calcul(), -1)
