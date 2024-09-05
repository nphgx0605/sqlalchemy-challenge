# Import the dependencies.
from flask import Flask, jsonify 
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import pandas as pd

app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Users/phuongnguyen/Desktop/sqlalchemy-challenge/sqlalchemy-challenge/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Routes
#################################################

# Home route
@app.route("/")
def home():
    print("Server received request for 'Home' page")
    return "Welcome to the 'Home' page!"

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year ago from the most recent date in the dataset
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the last 12 months of precipitation data
    precipitation_query = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).all()

    # Convert the query results to a DataFrame and then to a dictionary
    precipitation_df = pd.DataFrame(precipitation_query, columns=["date", "prcp"])
    precipitation_dict = precipitation_df.set_index("date").to_dict()["prcp"]

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    stations_data = session.query(Station.station).all()
    
    # Unravel results into a list
    stations_list = [station[0] for station in stations_data]

    # Return the JSONified list of stations
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Get the most recent date from the dataset
    one_year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    
    # Find the most active station
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]
    
    # Query the last 12 months of temperature observations for the most active station
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Convert results into a list of dictionaries
    temperature_list = [{"date": date, "tobs": tobs} for date, tobs in temperature_data]
    
    # Return the JSONified list of temperature observations
    return jsonify(temperature_list)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
