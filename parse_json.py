def func_parse_json(json_data, var_date):
    # Function takes as input data recieved via API for all countries for 1 date, parses and puts it into a list
    # API can't provide data for more than 3 or 4 months so we will make separate API calls for every date
    list1 = []
    countries_summary = []
    for var_country in json_data['data'][str(var_date)]:
        if str(json_data['data'][str(var_date)][var_country]['stringency_actual']) == 'None':
            var_stingency_actual = 'Not provided'
        else:
            var_stingency_actual = json_data['data'][str(var_date)][var_country]['stringency_actual']

        if str(json_data['data'][str(var_date)][var_country]['stringency']) == 'None':
            var_stingency = 'Not provided'
        else:
            var_stingency = json_data['data'][str(var_date)][var_country]['stringency']
        list1 = [str(var_date),
                 var_country,
                 json_data['data'][str(var_date)][var_country]['confirmed'],
                 json_data['data'][str(var_date)][var_country]['deaths'],
                 var_stingency_actual,
                 var_stingency
                 ]
        countries_summary.append(list1)
    return countries_summary
