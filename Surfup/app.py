# Import the dependencies.
from flask import Flask
from flask import jsonify 
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt

app = Flask(__name__)
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

# reflect an existing database into a new model
@app.route("/")
def home():
    print("Server received request for 'Home' page")
    return ("Welcome to 'Home' page")

# Save references to each table



# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
