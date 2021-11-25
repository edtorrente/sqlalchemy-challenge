
from matplotlib import style
from scipy import stats
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy	# Python SQL toolkit and Object Relational Mapper





#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found

Base.classes.keys()

# Save references to each table

measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return ("Welcome to Hawaii's Climate Page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/2016-02-15<br/>"
        f"/api/v1.0/start_date/end_date/2016-02-15/2016-02-25<br/>"

    )

#############################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using date as the key and prcp as the value."""
    # Query precipitation and dates
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Dictionary for key-value pairs date and prcp
    precipitation = []
    for _ in results:
        l = {}
        l[_[0]]= _[1]
        precipitation.append(_)
    return jsonify(precipitation)
################################################################
@app.route("/api/v1.0/tobs")
def tobs():

	#Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    # Calculate the date one year from the last date in data set, which is 2017-08-23.
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    _list = session.query(measurement.date, measurement.tobs).filter(measurement.date > year_ago).all()
    
    session.close()
    
    tobs_list = []
    for _ in results:
        l = {}
        l['date'] = _[1]
        l['temperature'] = _[0]
        tobs_list.append(l)
    return jsonify(tobs_list)
##############################################################
@app.route("/api/v1.0/max_min_avg/<start>")
def start(start):
    #Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for 
    a given start or start-end range."""
    
    #just in case date format is not yy-mm-dd
    new_start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    
    start_date = session.query(func.max(measurement.tobs). func.min(measurement.tobs), func.avg(measurement.tobs)).\
                              filter(measurement.date > new_start_dt).all()
    
    session.close()
    
    #list to hold results
    
    temp_list = []
    for _ in results:
        l = {}
        l['startdate'] = start_date
        l['min'] = _[0]
        l['max'] = _[1]
        l['avg'] = _[2]
        temp_list.append(l)
        
    return jsonify(temp_list)

#############################################################
@app.route("/api/v1.0/max_min_avg/<start>/<end>")

def start_ending(start, end):
    #Create our session (link) from Python to the DB
    session = Session(engine)
    
    """When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start 
    and end date inclusive."""
    
    start = dt. datetime.striptime(start, '%Y-%m-%d')
    end = dt. datetime.striptime(end, '%Y-%m-%d')
    
    #query data to find start date
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start_dt).filter(measurement.date <= end_dt)
    
    session.close()
    
    #list to hold results
    
    temp_list = []
    for _ in results:
        l = {}
        l['startdate'] = start
        l['enddate'] =  end
        l['min'] = _[0]
        l['max'] = _[1]
        l['avg'] = _[2]
        temp_list.append(l)
        
    return jsonify(temp_list)

###################################################################

if __name__ == 'main':
    app.run(debug=True)
    
    











