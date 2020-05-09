
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    last12 = dt.date(2017,8,22) - dt.timedelta(days=365)
    results = session.query(Measurement.prcp,Measurement.date).\
    filter(Measurement.date>last12).all()


    session.close()

    all_prcp = []
    for prcp,date in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
    
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    stations = session.query(Measurement.station).\
            group_by(Measurement.station).\
            all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    last12 = dt.date(2017,8,22) - dt.timedelta(days=365)
    session = Session(engine)

    
    
    tempobs= session.query(Measurement.tobs).\
        filter(Measurement.date >=last12).\
        filter(Measurement.station=="USC00519281").\
        all()

    session.close()

    # Convert list of tuples into normal list
    all_tempobs = list(np.ravel(tempobs))

    return jsonify(all_tempobs)

@app.route("/api/v1.0/<start>")
def startdate(start):
  
    session = Session(engine)


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    
    all_temps = list(np.ravel(results))

    return jsonify(all_temps)



@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
   
    session = Session(engine)


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date < end).all()
    session.close()
    
    all_temps = list(np.ravel(results))

    return jsonify(all_temps)

if __name__ == "__main__":
    app.run(debug=True)

