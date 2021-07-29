# importing flask
#localhost:500<url>
from flask import Flask
from flask import jsonify

# Importing SQL Alchemy ORM
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine , func

# Importing date functions
import datetime as dt
from datetime import datetime
from datetime import timedelta


# Setting up connection to the hawaii.sqlite database

# Defining engine
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine , reflect = True)

# Creating references for the tables in the database
stations = Base.classes.station

precip = Base.classes.measurement



# Creating our flask routes

# Defining an app
app = Flask(__name__);

# List the availible routes
@app.route('/')
def home():
    precip_route = '/api/v1.0/precipitation';
    station_route = '/api/v1.0/stations';
    tobs_route = '/api/v1.0/tobs';
    date_route = '/api/v1.0/<start>'
    date_range_route = '/api/v1.0/<start>/<end>'

    route_dict = {
        'precipitation': precip_route ,
        'stations': station_route , 
        'temp': tobs_route ,
        'date' : date_route ,
        'date_range': date_range_route
    }

    return jsonify(route_dict)


# Defining the precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Creating session
    session = Session(engine)

    # Querying measurement table for date and prcp columns
    precip_query = session.query(precip.date , precip.prcp).all()

    session.close()

    # defining dictionary structure
    precip_dict = {
        'Date': [] ,
        'precip' : []
    }

    for row in precip_query:
        precip_dict['Date'].append(row.date);
        precip_dict['precip'].append(row.prcp);


    return jsonify(precip_dict)

# Defining station route
@app.route('/api/v1.0/stations')
def station():
    session = Session(engine)

    station_query = session.query(stations.station).all()

    session.close()

    # Dict
    station_dict = {
        'Station': []
    }

    for row in station_query:
        station_dict['Station'].append(row.station)
    
    return jsonify(station_dict)

# defining tobs route
@app.route('/api/v1.0/tobs')
def tobs():

    # Referencing the dates
    recent_date = '2017-08-23'
    start_date = dt.datetime.strptime(recent_date , '%Y-%m-%d')
    end_date = start_date - dt.timedelta(days = 365)
    session = Session(engine)

    # Forming the query
    most_active_query = session.query(precip).filter(precip.station == 'USC00519281')\
    .filter(precip.date\
        .between(dt.datetime.strftime(end_date , '%Y-%m-%d') , dt.datetime.strftime(start_date , '%Y-%m-%d'))).all()
    
    # Defining dict

    most_active_dict = {
        'Temp': []
    }

    # Populating the query
    for row in most_active_query:
        most_active_dict['Temp'].append(row.tobs)



    return jsonify(most_active_dict)

# Defining route with start and end date
@app.route('/api/v1.0/<some_date>')
def date_func(some_date):

    session = Session(engine)


    max_temp = session.query(precip , func.max(precip.tobs)).filter(precip.station == 'USC00519281' ).filter(precip.date >= some_date).all()
    min_temp = session.query(precip , func.min(precip.tobs)).filter(precip.station == 'USC00519281').filter(precip.date >= some_date).all()
    avg_temp = session.query(precip , func.avg(precip.tobs)).filter(precip.station == 'USC00519281').filter(precip.date >= some_date).all()

    # defining dict

    stats_dict = {
        'max': max_temp[0][1] ,
        'min': min_temp[0][1] ,
        'avg': avg_temp[0][1]
    }

    return jsonify(stats_dict)













if __name__ == '__main__':
    app.run(debug = True)

