# Import Flask
from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create an app
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def allroutes():
    return (
        f"Available routes"
        )

@app.route("/api/v1.0/precipitation")
def dateandprecip():
    precip_analysis = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-24").\
    filter(measurement.date <= "2017-08-23").all()

    precip_dict = {date: prcp for date, prcp in precip_analysis}

    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    most_active = station_activity = session.query(measurement.station, station.name, func.count(measurement.tobs)).\
    filter(measurement.station == station.station).group_by(measurement.station).order_by(func.count(measurement.tobs).desc()).all()

    station_list = list(most_active)

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def stations():

    last_twelve = session.query(measurement.tobs).filter(measurement.station == "USC00519281").filter(measurement.date >= "2016-08-24").\
    filter(measurement.date <= "2017-08-23").all()

    last_twelve_list = list(last_twelve)

    return jsonify(last_twelve_list)

# Query analysis
@app.route("/api/v1.0/<start>")
def stations():


    if __name__ == "__main__":
        app.run(debug=True)