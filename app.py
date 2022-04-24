import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Define Flask app
app = Flask(__name__)

# Define the root route as welcome route
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br />
    Available Routes: <br />
    /api/v1.0/precipitation <br />
    /api/v1.0/stations <br />
    /api/v1.0/tobs <br />
    /api/v1.0/temp/start/end <br />
    ''')
    
# Route for the precipitation analysis.
# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
#Starting from the last data point in the database. 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in data set.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    precipitation  = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    
    # Format the results into a JSON structure
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Stations Route
# Returns a list of all stations
@app.route("/api/v1.0/stations")
def stations():
    # List the stations 
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


# Temperature Observations Route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    # Calculate the date one year from the last date in data set.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Using the station id from the most active station, calculate the lowest temperature recorded, # highest temperature recorded, and average temperature 
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    # Convert to list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Route for summary statistics report. Returns the minimum, maximum, and average temperatures within a given range
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # if no endpoint is defined, get all results after the start date
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    
    # Return all results between start and end date
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
    
    
    
    
    
    
    
    
    
    
    
    
    
