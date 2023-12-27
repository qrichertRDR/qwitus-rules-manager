# ---
# Name: Option End Date Rule
# Short Name: option_end_date_rule
# Type: ending
# ---

birth_year = date_de_naissance().timetuple()[0]
if param_age_kind() == 'real':
    return date_de_naissance() + relativedelta(
        years=param_max_age_for_option() + 1, days=-1)
elif param_age_kind() == 'at_end_of_month':
    birthday_month_after = date_de_naissance() + relativedelta(
        years=param_max_age_for_option() + 1, months=1)
    year, month, _ = birthday_month_after.timetuple()[0:3]
    first_day_following_month = datetime.date(year, month,
        1)
    return first_day_following_month + relativedelta(days=-1)
elif param_age_kind() == 'at_given_day_of_year':
    given_date_in_birth_year = datetime.date(birth_year,
        int(param_given_month()), int(param_given_day()))
    if date_de_naissance() >= given_date_in_birth_year:
        return given_date_in_birth_year + relativedelta(
            years=param_max_age_for_option() + 1, days=-1)
    else:
        return given_date_in_birth_year + relativedelta(
            years=param_max_age_for_option(), days=-1)
