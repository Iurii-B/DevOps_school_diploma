from flask import Flask, render_template, redirect, request
from sqlalchemy import create_engine, Column, String, Integer, Sequence, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.request import urlopen
from datetime import date, timedelta
from time import strptime
from json import loads
import os


def func_parse_json(json_data, var_date):
    # Function takes as input data received via API for all countries for 1 date, parses and puts it into a list
    # API can't provide data for more than 3 or 4 months, so we will make separate API calls for every date
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


url_no_date = 'https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/'
start_2021_date = date(year=2021, month=1, day=1)
end_date = date.today() - timedelta(days=355)


'''
var_date = start_2021_date
while var_date < end_date:
    url_with_date = url_no_date + str(var_date) + '/' + str(var_date)
    response = urlopen(url_with_date)
    json_data = loads(response.read())
    # "json_data" is a list of statistics for all countries for a single date
    # [['2021-12-10', 'AGO', 65371, 1737, 66.67, 66.67], ['2021-12-10', 'ALB', 203215, 3130, 45.37, 45.37], ...]
    total_year_data.append(func_parse_json(json_data, var_date))
    var_date = var_date + timedelta(days=1)
'''

#print(func_parse_json(json_data, var_date))
#print(total_year_data)


def func_populate_or_update_db(var_date, end_date):
    # Usually "end_date" is set to Yesterday; see beginning of the code
    total_year_data = []  # Adjustment for variant without DB
    while var_date < end_date:
        # API can't provide data for more than a couple of months, so we will make separate API calls for every day
        url_with_date = url_no_date + str(var_date) + '/' + str(var_date)
        try:
            response = urlopen(url_with_date)
            json_data = loads(response.read())
            json_data_data_key = json_data['data']
        except KeyError:
            print(json_data, var_date)
            var_date = var_date + timedelta(days=1)
            continue
        # Call function "func_insert_db" to insert into DB parsed data that was obtained via API
        #func_insert_db(func_parse_json(json_data, var_date))
        # Call function "func_parse_json" to parse data for the date of the current iteration
        # and append it to a summary list "total_year_data"
        total_year_data.append(func_parse_json(json_data, var_date))  # For variant without DB
        var_date = var_date + timedelta(days=1)
    #return None
    return total_year_data  # For variant without DB

a = func_populate_or_update_db(start_2021_date, end_date)
