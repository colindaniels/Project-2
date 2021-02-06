from flask import Flask, render_template, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/weatherCOVID'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#create / use table

with open('templates/build/counties.json') as file:
    json_data = json.load(file)


class json_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    json_column = db.Column(JSON)
db.create_all()

def insert_json():
    json_column = json_table(json_column=json_data)
    db.session.add(json_column)
    db.session.commit()
insert_json()

class combined_data(db.Model):
    index = db.Column(db.BIGINT, primary_key=True)
    date = db.Column(db.TEXT)
    tempf = db.Column(db.BIGINT)
    latitude = db.Column(db.TEXT)
    longitude = db.Column(db.TEXT)
    county = db.Column(db.TEXT)
    state = db.Column(db.TEXT)
    cases = db.Column(db.BIGINT)
    deaths = db.Column(db.BIGINT)
    new_fips = db.Column(db.BIGINT)
results = combined_data.query.all()
json_results = json_table.query.all()



all_data = {'index': [result.index for result in results],
            'date': [result.date for result in results],
            'tempf': [result.tempf for result in results],
            'latitude': [result.latitude for result in results],
            'longitude': [result.longitude for result in results],
            'county': [result.county for result in results],
            'state': [result.state for result in results],
            'cases': [result.cases for result in results],
            'deaths': [result.deaths for result in results],
            'fips': [result.new_fips for result in results],
            'json': [result.json_column for result in json_results]
            }

@app.route("/")
def index():
    return render_template('index.html', data=all_data)

@app.route("/county_data")
def county():
    return jsonify(all_data['json'])

@app.route("/overTimeData")
def overTimeData():
    return render_template('overTimeData.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
