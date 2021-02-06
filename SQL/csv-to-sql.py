# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 17:12:14 2021

@author: Mason
"""

from sqlalchemy import create_engine, Numeric
import pandas
from config import password

engine = create_engine("postgresql://postgres:password@localhost/weatherCOVID")

DF = pandas.read_csv("../AdjustedFinal.csv", header=0)
#weatherDF = pandas.read_csv("../CleanedWeatherData.csv", header=0)


DF.to_sql("combined_data", con=engine, if_exists="replace")
engine.execute("SELECT * FROM combined_data").fetchall()
print("Table updated!")