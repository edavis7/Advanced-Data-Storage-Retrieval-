import sqlalchemy 
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)


Measurement = Base.classes.meaaurement
Station = Base.classes.Station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page.")
    return "Welcome to Surfs Up: Hawaii's Weather!"

@app.route("/Welcome")
def welcome ():
    return(
        f"Welcome to Surfs Up: Hawaii's Weather<br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")  
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()
    trip_prcp = list(np.ravel(results))
    
    trip_prcp = []
    for results in results:
        prcp_dict = {}
        prcp_dict[Measurement.date] = prcp_dict[Measurement.prcp]
        
        trip_prcp.append(prcp_dict)
    return jsonify(prcp_dict)

@app.route("api/v1.0/stations")  
def station():
    results = session.query(Station.station).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("api/v1.0/tobs")  
def temperature():
    year_tobs = []
    results = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()

    year_tobs = list(np.ravel(results))      
    return jsonify(year_tobs)

@app.route("api/v1.0/<start>")
def starttrip(start_date):
    start_temp = []
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    start_temp = list(np.ravel(results))
    return jsonify(start_temp)

@app.route("api/v1.0/<start>/<end>")    
def startendtrip(start_date, end_date): 
    startend_temps = []
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    startend_temps = list(np.ravel(results))
    return jsonify(startend_temps)

if __name__ == '__main__':
    app.run(debug=True)