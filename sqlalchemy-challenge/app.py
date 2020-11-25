import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

## Home Route:
@app.route("/")
def home():
    return ( 
    f"Routes:<br />"
    f"<br />"
    f"/api/v1.0/precipitation<br />"
    f"/api/v1.0/stations<br />"
    f"/api/v1.0/tobs<br />"
    f"/api/v1.0/start<br />"
    f"/api/v1.0/start/end<br />"
    )


## Precipitation Route:
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value
        # Calculate the Date 1 Year Ago from the Last Data Point in the Database
        last_date = dt.date(2017, 8, 23)
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).\
                    order_by(Measurement.date).all()
        # Convert List of Tuples Into a Dictionary
        prcp_data_list = dict(prcp_data)
        # Return JSON Representation of Dictionary
        return jsonify(prcp_data_list)


## Stations Route:
@app.route("/api/v1.0/stations")
def station():
        # Return a JSON List of Stations From the Dataset
        stations_all = session.query(Station.station, Station.name).all()
        # Convert List of Tuples Into Normal List
        station_list = list(stations_all)
        # Return JSON List of Stations from the Dataset
        return jsonify(station_list)


## Temperature (tobs) Route:
@app.route("/api/v1.0/tobs")
def tobs(): 
        # Calculate the Date 1 Year Ago from the Last Data Point in the Database
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Value
        active_station_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).\
        filter(Measurement.station == "USC00519281").\
        order_by(Measurement.date).all()
         # Convert List of Tuples Into Normal List
        tobs_list = list(active_station_query)
        # Return JSON List of Temperature Observations (tobs) for the Previous Year for the Most Active Station
        return jsonify(tobs_list)


## Start Day Route:
@app.route("/api/v1.0/<start>")
def single_date(start):
    # Set up for user to enter date
    start_date = dt.date(2016, 8, 23)

    # Query Min, Max, and Avg based on date
    summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),\
                    func.round(func.avg(Measurement.tobs))).\
                    filter(Measurement.date >= start_date).all()
    
    # Convert List of Tuples Into Normal List
    summary = list(np.ravel(summary_stats))

    # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
    return jsonify(summary)
    
# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def trip_dates(start,end):
    # Set up for user to enter dates 
    start_date = dt.date(2016, 8, 23)
    end_date = dt.date(2017, 8, 23)

    # Query Min, Max, and Avg based on dates
    summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),\
                    func.round(func.avg(Measurement.tobs))).\
                    filter(Measurement.date >= start_date).\
                    filter(Measurement.date <= end_date).\
                    group_by(Measurement.date).all()
    
    # Convert List of Tuples Into Normal List
    summary = list(np.ravel(summary_stats))

    # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
    return jsonify(summary)

    
if __name__ == "__main__":
    app.run(port=9000, debug=True)

        
        
        
        
        
        
        
        
        
        
        
        
        