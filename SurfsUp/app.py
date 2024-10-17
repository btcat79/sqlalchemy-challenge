from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

## Step 4: Setting Up the Flask Application
We initialize a Flask web application, which will serve as our API. This application will define multiple endpoints that users can access to query different types of climate data.
Markdown Cell 6: Defining Flask Routes

# Create Flask app
app = Flask(__name__)

# Set up the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link
session = Session(engine)

## Step 5: Defining API Routes

In this section, we define the endpoints for the Flask application. Each route will correspond to a different type of query that can be made against the climate database. The routes will include:
1. The homepage, which lists all available endpoints.
2. A route for querying precipitation data.
3. A route for listing available weather observation stations.
4. A route for retrieving temperature data for a specific station.
5. A route for getting temperature statistics within a specified date range.


### Home Route
This is the default route of our API. It provides a list of all available endpoints, which allows users to navigate to the desired data queries. Each endpoint is described with the corresponding URL path and expected output.


### Precipitation Data Route
This route returns a JSON dictionary containing the precipitation data for each date in the dataset. The data is structured as a key-value pair, where the key is the date, and the value is the precipitation amount.

### Stations Route
This endpoint returns a JSON list of all weather observation stations available in the database. Each station represents a specific location where weather observations have been recorded.

### Temperature Observations Route
This route provides a JSON list of temperature observations (TOBs) for the most active weather station over the past year. It retrieves the last 12 months of temperature data.




# Set up the homepage route
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Route for temperature statistics from the start date
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Query minimum, average, and maximum temperature from the start date to the end of the dataset
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Create a dictionary for the results
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    # Return the JSON representation of the dictionary
    return jsonify(temp_stats)

### Start and End Date Temperature Statistics
This endpoint returns a JSON dictionary containing the minimum, average, and maximum temperatures for a given date range. If only the start date is provided, it calculates statistics for all data points after that date. If both start and end dates are provided, it calculates statistics within that range.


# Route for temperature statistics from the start date to the end date
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Query minimum, average, and maximum temperature for the specified date range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Create a dictionary for the results
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    # Return the JSON representation of the dictionary
    return jsonify(temp_stats)

# Ensure that the Flask app runs
if __name__ == "__main__":
    app.run(debug=True)
