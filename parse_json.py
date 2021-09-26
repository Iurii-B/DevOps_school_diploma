def func_parse_json(json_data, var_date):
    # Function takes as input data recieved via API for all countries for 1 date, parses and puts it into a list
    # API can't provide data for more than 3 or 4 months so we will make separate API calls for every date
    list1 = []
    countries_summary_get_json = []
    for var_country in json_data['data'][str(var_date)]:
        if str(json_data['data'][str(var_date)][var_country]['confirmed']) == 'None':
            var_confirmed = 0
        else:
            var_confirmed = json_data['data'][str(var_date)][var_country]['confirmed']

        if str(json_data['data'][str(var_date)][var_country]['deaths']) == 'None':
            var_deaths = 0
        else:
            var_deaths = json_data['data'][str(var_date)][var_country]['deaths']

        if str(json_data['data'][str(var_date)][var_country]['stringency_actual']) == 'None':
            var_stringency_actual = 'Not provided'
        else:
            var_stringency_actual = json_data['data'][str(var_date)][var_country]['stringency_actual']

        if str(json_data['data'][str(var_date)][var_country]['stringency']) == 'None':
            var_stringency = 'Not provided'
        else:
            var_stringency = json_data['data'][str(var_date)][var_country]['stringency']
        list1 = [str(var_date),
                 var_country,
                 var_confirmed,
                 var_deaths,
                 var_stringency_actual,
                 var_stringency
                 ]
        countries_summary_get_json.append(list1)
    return countries_summary_get_json
