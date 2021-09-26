from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine, Column, String, Integer, Sequence, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.request import urlopen
from datetime import date, timedelta
from json import loads
import keyring
from parse_json import func_parse_json

app = Flask(__name__)

url_no_date = 'https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/'
start_2021_date = date(year=2021, month=1, day=1)
end_date = date.today() - timedelta(days=95)


db = create_engine("postgresql://db_admin:"+keyring.get_password("keyring_creds_01", "db_admin")+"@localhost/postgres")


Base = declarative_base()
# Creating a parent class of SQLAlchemy ORM


ID_SEQ = Sequence('id_seq')


class Covid1(Base):
    __tablename__ = 'covid_1'
    id = Column(Integer, ID_SEQ, primary_key=True, server_default=ID_SEQ.next_value())
    date = Column(Date)
    country = Column(String)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    stringency_actual = Column(String)
    stringency = Column(String)


Base.metadata.create_all(db)

Session = sessionmaker(db)
session = Session()



def func_insert_db(countries_summary_get_json):
    # Function to insert records into database
    # "countries_summary" is a list of lists, containing statistics for 1 country for 1 date; example:
    # [['2021-01-01', 'ABW', 5509, 49, 35.19, 35.19], ['2021-01-01', 'AFG', 52513, 2201, 12.04, 12.04]]
    for j in countries_summary_get_json:
        x = Covid1(date=j[0], country=j[1], confirmed=j[2], deaths=j[3], stringency_actual=j[4], stringency=j[5])
        session.add(x)
        session.commit()


def func_check_latest_record(table_name):
    i = date(year=2021, month=1, day=1)
    while i < date.today():
        try:
            var_tmp_1 = session.query(table_name).filter(table_name.country == 'USA', table_name.date == i).first()
            # If there is no record for specific date, attempt to get any record for it will cause Exception
            var_tmp_2 = var_tmp_1.date
            i = i + timedelta(days=1)
        except AttributeError:
            break
    return i   # "i" will be the first date for which there is NO record


def func_populate_or_update_db(var_date, end_date):
    # Usually "end_date" is set to Yesterday; see beginning of the code
    while var_date <= end_date:
        # API can't provide data for more than 3 or 4 months so we will make separate API calls for every day
        url_with_date = url_no_date + str(var_date) + '/' + str(var_date)
        response = urlopen(url_with_date)
        json_data = loads(response.read())
        # Call function to insert into DB parsed data that was obtained via API
        func_insert_db(func_parse_json(json_data, var_date))
        var_date = var_date + timedelta(days=1)
    return None


func_populate_or_update_db(func_check_latest_record(Covid1), end_date)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/country/<country_id>')
def country_detail(country_id):
    country_detail_read_db = []
    list1 = []
    var_latest_date = func_check_latest_record(Covid1) - timedelta(days=1)
    for i in session.query(Covid1).filter(Covid1.country == str(country_id).upper()).order_by(Covid1.deaths):
        list1 = [str(i.date),
                 i.country,
                 i.confirmed,
                 i.deaths,
                 i.stringency_actual,
                 i.stringency
                 ]
        country_detail_read_db.append(list1)
    return render_template('country_detail.html', country_detail_read_db=country_detail_read_db)


@app.route('/list')
def countries_list():
    # On this page we display statistics for all countries for the latest available date
    # "countries_summary_read_db" is a list of lists, containing statistics for 1 country for 1 date; example:
    # [['2021-01-01', 'ABW', 5509, 49, 35.19, 35.19], ['2021-01-01', 'AFG', 52513, 2201, 12.04, 12.04]]
    # The difference from "countries_summary_get_json" is that in "countries_summary_read_db" this list is being
    # extracted from DB, not pulled via API from the Internet
    countries_summary_read_db = []
    list1 = []
    var_latest_date = func_check_latest_record(Covid1) - timedelta(days=1)
    for i in session.query(Covid1).filter(Covid1.date == var_latest_date).order_by(Covid1.deaths):
        list1 = [str(i.date),
                 i.country,
                 i.confirmed,
                 i.deaths,
                 i.stringency_actual,
                 i.stringency
                 ]
        countries_summary_read_db.append(list1)

    return render_template('countries_list.html', countries_summary_read_db=countries_summary_read_db)



@app.route('/update')
def data_update():
    # Update DB while staying on the same page
    func_populate_or_update_db(func_check_latest_record(Covid1), end_date)
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), host="0.0.0.0")