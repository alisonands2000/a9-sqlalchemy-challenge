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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
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

prcp_dict = {d:p for d, p in past_year_data}

#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
@app.route("/")
def main():
    return '''
        <h2>Available routes:</h2>
        /api/v1.0/precipitation<br>
        /api/v1.0/stations<br>
        /api/v1.0/tobs<br>
        /api/v1.0/[start] and /api/v1.0/[start]/[end]
    '''

@app.route("/api/v1.0/precipitation")
def prcp():
    print(prcp_dict)
    return prcp_dict

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station, station.name).all()
    stations_list = {id:loc for id, loc in stations}
    return stations_list

@app.route("/api/v1.0/tobs")
def most_active_station():
    most_active_station = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(desc(func.count(measurement.station))).first()
    # most_active_station_id = most_active_station[0]
    most_active_station_latest_date = session.query(measurement.date).order_by(desc(measurement.date)).first()
    most_active_station_latest_date = dt.datetime.strptime(most_active_station_latest_date[0], '%Y-%m-%d')
    # most_active_station_past_year = most_active_station_latest_date - dt.timedelta(365)
    most_active_station_past_year_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= past_year).all()
    # prcp_df = pd.DataFrame(most_active_station_past_year_data, columns = ['date', 'temp'])
    tobs = {d:t for d,t in most_active_station_past_year_data}
    return tobs

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end = '2017-08-23'):
    session = Session(engine)

    [min,avg,max] = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter((measurement.date>=start)&(measurement.date<=end)).first()
    return {'Min':min,'AVG':avg,'Max':max}


if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/api/v1.0/<start>")


# @app.route("/api/v1.0/<start>/<end>")