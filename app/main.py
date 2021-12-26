from flask import Flask, render_template, redirect, request
from sqlalchemy import create_engine, Column, String, Integer, Sequence, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.request import urlopen
from datetime import date, timedelta
from time import strptime
from json import loads
import os


app = Flask(__name__)


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


def func_sql_to_python_date(sql_row_date):
    # Convert data formats because when querying DB with command "session.query(func.max(Covid1.date)).first())",
    # the date is returned in "(datetime.date(2021, 10, 21),)" format of class "<class 'sqlalchemy.engine.row.Row'>"
    python_date = start_2021_date
    python_date = date(year=strptime(str(sql_row_date)[15:].replace('),)', ''), '%Y, %m, %d').tm_year,
                       month=strptime(str(sql_row_date)[15:].replace('),)', ''), '%Y, %m, %d').tm_mon,
                       day=strptime(str(sql_row_date)[15:].replace('),)', ''), '%Y, %m, %d').tm_mday)
    return python_date

'''
def func_insert_db(countries_summary_get_json):
    # Function to insert records into database
    # "countries_summary" is a list of lists, each containing statistics for 1 country for 1 date; example:
    # [['2021-01-01', 'ABW', 5509, 49, 35.19, 35.19], ['2021-01-01', 'AFG', 52513, 2201, 12.04, 12.04]]
    for j in countries_summary_get_json:
        x = Covid1(date=j[0], country=j[1], confirmed=j[2], deaths=j[3], stringency_actual=j[4], stringency=j[5])
        session.add(x)
        session.commit()
'''

def func_populate_or_update_db(var_date, end_date):
    # Usually "end_date" is set to Yesterday; see beginning of the code
    total_year_data = []  # Adjustment for variant without DB
    while var_date < end_date:
        # API can't provide data for more than a couple of months, so we will make separate API calls for every day
        url_with_date = url_no_date + str(var_date) + '/' + str(var_date)
        try:
            response = urlopen(url_with_date)
            json_data = loads(response.read())
            # "json_data" is a list of statistics for all countries for a single date
            # [['2021-12-10', 'AGO', 65371, 1737, 66.67, 66.67], ['2021-12-10', 'ALB', 203215, 3130, 45.37, 45.37], ...]
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


url_no_date = 'https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/'
start_2021_date = date(year=2021, month=1, day=1)
end_date = date.today() - timedelta(days=355)

'''
engine = create_engine("mariadb+mariadbconnector://"+os.environ.get('DB_ADMIN_USERNAME')+":"+os.environ.get('DB_ADMIN_PASSWORD')+"@"+os.environ.get('DB_URL')+"/database1"+"", pool_pre_ping=True, isolation_level="READ UNCOMMITTED")
# engine = create_engine("postgresql://" + os.environ.get('DB_ADMIN_USERNAME') + ":"+os.environ.get('DB_ADMIN_PASSWORD')+"@"+os.environ.get('DB_URL_POSTGRES')+"")
# Connecting to the database "postgres" or "database1"; the database itself should already exist, the app will not
# create database itself. But the app will create tables in the database if they do not exist.


Base = declarative_base()
# Creating a declarative base class that stores a catalog of classes and mapped tables in the Declarative system


ID_SEQ = Sequence('id_seq')  # Special object to generate unique IDs in the database


class Covid1(Base):
    __tablename__ = 'covid_1'  # Actual name of the table in the database
    id = Column(Integer, ID_SEQ, primary_key=True, server_default=ID_SEQ.next_value())
    date = Column(Date)
    country = Column(String(30))
    confirmed = Column(Integer)
    deaths = Column(Integer)
    stringency_actual = Column(String(30))
    stringency = Column(String(30))


Base.metadata.create_all(engine)  # Creating table in the database


Session = sessionmaker(engine)  # Defining a special Session class
session = Session()  # Creating an object of Session class


func_populate_or_update_db(func_sql_to_python_date(session.query(func.max(Covid1.date)).first()) + timedelta(days=1), end_date)
session.close()
engine.dispose()
# We check the latest available record in DB (MAX.date) and start populating DB from the next day
'''


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

'''
@app.route('/country/<country_id>')
def country_detail(country_id):
    country_detail_read_db = []
    for i in session.query(Covid1).filter(Covid1.country == str(country_id).upper()).order_by(Covid1.deaths):
        list1 = [str(i.date),
                 i.country,
                 i.confirmed,
                 i.deaths,
                 i.stringency_actual,
                 i.stringency
                 ]
        country_detail_read_db.append(list1)
        session.close()
        engine.dispose()
    return render_template('country_detail.html', country_detail_read_db=country_detail_read_db)


@app.route('/list')
def countries_list():
    countries_summary_read_db = []
    var_latest_date = func_sql_to_python_date(session.query(func.max(Covid1.date)).first())
    for i in session.query(Covid1).filter(Covid1.date == var_latest_date).order_by(Covid1.deaths):
        list1 = [str(i.date),
                 i.country,
                 i.confirmed,
                 i.deaths,
                 i.stringency_actual,
                 i.stringency
                 ]
        countries_summary_read_db.append(list1)
        session.close()
        engine.dispose()
    return render_template('countries_list.html', countries_summary_read_db=countries_summary_read_db)


@app.route('/update')
def data_update():
    # Update DB while staying on the same page
    func_populate_or_update_db(func_sql_to_python_date(session.query(func.max(Covid1.date)).first()) + timedelta(days=1), end_date)
    session.close()
    engine.dispose()
    return redirect(request.referrer)
'''


if __name__ == "__main__":
    app.run(host="0.0.0.0")
