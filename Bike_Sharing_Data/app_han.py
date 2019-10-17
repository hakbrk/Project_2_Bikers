import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bikers.db"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Trip=Base.classes.filtered_trip
Location=Base.classes.Austin_B_Cycle_Kiosk_Locations


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/data")
def getdata():
    trip_query=db.session.query(Trip).statement
    df=pd.read_sql_query(trip_query,db.session.bind)

    def process(df, year):
        df1=df[df["Year"]==year]
        checkout=df1["Checkout Kiosk ID"].value_counts()
        Return=df1["Return Kiosk ID"].value_counts()
        c_df=pd.DataFrame({"c_count":checkout})
        r_df=pd.DataFrame({"r_count":Return})
        c_df.reset_index(drop=False,inplace=True)
        r_df.reset_index(drop=False,inplace=True)
        merge=pd.merge(c_df,r_df,on="index",how="outer")
        merge["Year"]=year
        merge["Count"]=merge["c_count"]+merge["r_count"]
        df2=merge[["index","Count","Year"]]
        df2=df2.rename(columns={"index":"kiosk_id"})
        df2.sort_values(["kiosk_id"],inplace=True)
        df2.reset_index(drop=True,inplace=True)
        return df2

    df_14=process(df,2014)
    df_15=process(df,2015)
    df_16=process(df,2016)
    df_all=pd.concat([df_14,df_15,df_16])
    df_all.reset_index(drop=True,inplace=True)

    location_query=db.session.query(Location).statement
    kiosk_df=pd.read_sql_query(location_query,db.session.bind)
    kiosk_df=kiosk_df[["Kiosk ID", "Latitude","Longitude","Kiosk Name"]]
    data_df=pd.merge(df_all,kiosk_df,left_on="kiosk_id",right_on="Kiosk ID")
    final_data=data_df[["Kiosk ID","Count","Year","Latitude","Longitude", "Kiosk Name"]]
    data_json=final_data.to_json(orient="records")
    return data_json


if __name__ == "__main__":
    app.run()
