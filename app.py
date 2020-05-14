# 1. import Flask
from flask import Flask

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes

# Base.metadata.tables # Check tables, not much useful
# Base.classes.keys() # Get the table names

Measurement = Base.classes
Station = Base.classes


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# 2. Create an app, being sure to pass __name__

app = Flask(__name__)

# 3. Define what to do when a user hits the index route

@app.route("/")
def allroutes():
    return (
        f"Available routes"
        )

@app.route("/api/v1.0/precipitation")
def dateandprecip():
    precip_analysis = Session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-24").\
    filter(Measurement.date <= "2017-08-23").all()

    precip_dict = {date: prcp for date, prcp in precip_analysis}

    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def most_active():
    most_active = Session.query(Measurement.station, Station.name, func.count(Measurement.tobs)).\
    filter(Measurement.station == Station.station).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).all()

    station_list = list(most_active)

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def last_twelve():

    last_twelve = Session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= "2016-08-24").\
    filter(Measurement.date <= "2017-08-23").all()

    last_twelve_list = list(last_twelve)

    return jsonify(last_twelve_list)


#similar to last query analysis from starter code
@app.route("/api/v1.0/<start>")
def temps_calculations_start():

    temps_calculations_start = Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= "2015-02-23").all()
    return jsonify(temps_calculations_start)

@app.route("/api/v1.0/<start>/<end>")
def temps_calculations_end():

    temps_calculations_start_end = Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= "2015-02-23").filter(Measurement.date <= "2015-03-01").all()
    return jsonify(temps_calculations_start_end)

if __name__ == "__main__":
    app.run(debug=True)