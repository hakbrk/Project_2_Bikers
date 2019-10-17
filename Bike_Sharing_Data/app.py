import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict

app = Flask(__name__)

#################################################
# Database Setup
#################################################
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trip_dates.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
trip_date = Base.classes.bike_data


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/Day")
def day():

    # Use Pandas to perform the sql query
    
    trip_query=db.session.query(trip_date).statement

    df=pd.read_sql_query(trip_query,db.session.bind)
    
    dayslist = df['day_of_week'].value_counts(dropna=False).keys().tolist()
    dayscountlist = df['day_of_week'].value_counts(dropna=False).tolist()
    days_dict = dict(zip(dayslist, dayscountlist))
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    days_dict = OrderedDict(sorted(days_dict.items(),key =lambda x:days.index(x[0])))
    newdaylist = list(days_dict.keys())
    newdaycount = list(days_dict.values())


    trace = {
        "x": newdaylist,
        "y": newdaycount,
        "type": "scatter",
        "fill": "tozeroy",
    }
    return jsonify(trace)

@app.route("/All")
def all():
    # Use Pandas to perform the sql query
    trip_query=db.session.query(trip_date).statement
    df=pd.read_sql_query(trip_query,db.session.bind)
    dates = df['Checkout Date'].value_counts(dropna=False).keys().tolist()
    datescount = df['Checkout Date'].value_counts(dropna=False).tolist()
    

    trace = {
        "x": dates,
        "y": datescount,
        "type": "bar",
        "fill": "tozeroy",
    }
    return jsonify(trace)

@app.route("/Month")
def month():
    # Use Pandas to perform the sql query
    trip_query=db.session.query(trip_date).statement
    df=pd.read_sql_query(trip_query,db.session.bind)
    monthslist = df['month'].value_counts(dropna=False).keys().tolist()
    monthcount = df['month'].value_counts(dropna=False).tolist()
    months_dict = dict(zip(monthslist, monthcount))
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    months_dict = OrderedDict(sorted(months_dict.items(),key =lambda x:months.index(x[0])))
    newmonthlist = list(months_dict.keys())
    newmonthcount = list(months_dict.values())
    print(newmonthlist)
    print(newmonthcount)

    trace = {
        "x": newmonthlist,
        "y": newmonthcount,
        "type": "scatter",
        "fill": "tozeroy",
    }
    return jsonify(trace)



@app.route("/options")
def options():
    options = ["All", "Month", "Day"]

    return jsonify(options)


if __name__ == "__main__":
    app.run()
