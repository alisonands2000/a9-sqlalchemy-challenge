# Import the dependencies.
from flask import Flask
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc, func

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

#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
@app.route("/")
def main():
    return "HEllo!"

# @app.route("/api/v1.0/precipitation")


# @app.route("/api/v1.0/stations")


# @app.route("/api/v1.0/tobs")

if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/api/v1.0/<start>")


# @app.route("/api/v1.0/<start>/<end>")