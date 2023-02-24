# Import necessary libraries
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import numpy as np
#create an engine 
engine = create_engine("sqlite:///hawaii.sqlite")

#refect an existing database 
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)

#save references
print(Base.classes.keys())
Measurement_T = Base.classes.measurement
Station_T = Base.classes.station

#flask set up
app = Flask(__name__)


@app.route("/")
def home():
    print("server recieved request for 'home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt<br/>"
    )
  
    #return "welcome to the surfing secret site"

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("server recieved request for 'precipitation' page...")
    #create session link to the Database
    session = Session(engine)

    date_12_months = dt.date(2016, 8, 22)

    precipitations = session.query(Measurement_T.date,Measurement_T.prcp).\
    filter(Measurement_T.date >= '2016-08-23').\
    order_by(Measurement_T.date).all()

    
    session.close()

    prcp_list = []

    for date, prcp in precipitations:
        prcp_dict = {date:prcp}

        prcp_list.append(prcp_dict)
        

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    print("server recieved request for 'stations' page...")
    session = Session(engine)
    results = session.query(Station_T.station)

    stations_list = [station[0] for station in results]
  

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    print("server recieved request for 'tobs' page...")
    # Get the date one year ago from the most recent date in the database
    session = Session(engine)
    


    # Query the database for the temperature observations of the most active station in the last year
    results = session.query(Measurement_T.date, Measurement_T.tobs)\
        .filter(Measurement_T.station == 'USC00519281')\
        .filter(Measurement_T.date >= '2016-08-23')\
        .all()

    # Convert the results to a dictionary and jsonify the response
    tobs_dict = {date: tobs for date, tobs in results}
    return jsonify(tobs_dict)
   


@app.route("/api/v1.0/&ltstart&gt")
def start_date(start):
    session = Session(engine) 

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""

    # Create query for minimum, average, and max tobs where query date is greater than or equal to the date the user submits in URL
                                        
    start_date_tobs_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()                                       
    
    session.close() 

    # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_date_tobs_values =[]
    for min, avg, max in start_date_tobs_results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min"] = min
        start_date_tobs_dict["average"] = avg
        start_date_tobs_dict["max"] = max
        start_date_tobs_values.append(start_date_tobs_dict)
    
    return jsonify(start_date_tobs_values)


# Create a route that when given the start date only, returns the minimum, average, and maximum temperature observed for all dates greater than or equal to the start date entered by a user

@app.route("/api/v1.0/<start>/<end>") 

# Define function, set start and end dates entered by user as parameters for start_end_date decorator
def Start_end_date(start, end):
    session = Session(engine)

    """Return a list of min, avg and max tobs between start and end dates entered"""
    
    # Create query for minimum, average, and max tobs where query date is greater than or equal to the start date and less than or equal to end date user submits in URL

    start_end_date_tobs_results = session.query(func.min(Measurement_T.tobs), func.avg(Measurement_T.tobs), func.max(Measurement_T.tobs)).\
        filter(Measurement_T.date >= start).\
        filter(Measurement_T.date <= end).all()

    session.close()
  
    # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_end_tobs_date_values = []
    for min, avg, max in start_end_date_tobs_results:
        start_end_tobs_date_dict = {}
        start_end_tobs_date_dict["min_temp"] = min
        start_end_tobs_date_dict["avg_temp"] = avg
        start_end_tobs_date_dict["max_temp"] = max
        start_end_tobs_date_values.append(start_end_tobs_date_dict) 
    

    return jsonify(start_end_tobs_date_values)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)

#@app.get('/shutdown')
#def shutdown():
   # shutdown_server()
   # return 'Server shutting down...'
