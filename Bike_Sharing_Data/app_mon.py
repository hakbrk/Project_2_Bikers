import os

import pandas as pd
import numpy as np


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/df_pie_all.sqlite'

db = SQLAlchemy(app)

Base = automap_base()

Base.prepare(db.engine, reflect=True)

Data_pie = Base.classes.df_pie_all

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/names")
def names():
    """Return a list of columns"""
    stmt = db.session.query(Data_pie).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    # df['column name'].values.tolist()
    year_list = df["Year"].unique()
    year_list_unique = year_list.tolist()
    return jsonify(year_list_unique)

@app.route("/samples/<year>")
def samples(year):
    stmt = db.session.query(Data_pie).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    selected_year = year

    year_data = df.loc[df["Year"] == int(selected_year),:]

    year_data_json = {
        "Membership": year_data["Membership"].tolist(),
        "Counts": year_data["Counts"].tolist(),
    }

    return jsonify(year_data_json)


if __name__ == "__main__":
    app.run()
