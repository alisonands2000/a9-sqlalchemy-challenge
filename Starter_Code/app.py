# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, desc, func
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################
app = Flask(__name__)

# reflect an existing database into a new model
# reflect the tables



# Save references to each table
engine = create_engine("sqlite:///Starter_Code/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with = engine)

measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# last 12 months of data
date = session.query(measurement.date).order_by(desc(measurement.date)).first()
past_year = dt.datetime.strptime(date[0], '%Y-%m-%d') - dt.timedelta(365)

past_year_data = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= past_year).all()
prcp_df = pd.DataFrame(past_year_data, columns = ['year', 'precipitation'])
prcp_dict = prcp_df.to_dict()

#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
@app.route("/")
def main():
    return "HEllo!"

@app.route("/api/v1.0/precipitation")
def prcp():
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station, station.name).all()
    stations_list = [[station[0], station[1]] for station in stations]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def most_active_station():
    most_active_station = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(desc(func.count(measurement.station))).first()
    # most_active_station_id = most_active_station[0]
    most_active_station_latest_date = session.query(measurement.date).order_by(desc(measurement.date)).first()
    most_active_station_latest_date = dt.datetime.strptime(most_active_station_latest_date[0], '%Y-%m-%d')
    # most_active_station_past_year = most_active_station_latest_date - dt.timedelta(365)
    most_active_station_past_year_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= past_year).all()
    prcp_df = pd.DataFrame(most_active_station_past_year_data, columns = ['date', 'temp'])
    return (f"The most active station is {most_active_station}", prcp_df.values.tolist())


if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/api/v1.0/<start>")


# @app.route("/api/v1.0/<start>/<end>")