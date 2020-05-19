from flask import Flask, render_template, request, jsonify
import pandas as pd
import json

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    global confirmed, deaths, recovered, data
    if request.method == 'POST':
        if request.form['data'] == 'Confirmed':
            to_send = {
                'value': confirmed.to_json(orient='index'),
                'size': confirmed.shape[0],
            }
        elif request.form['data'] == 'Deaths':
            to_send = {
                'value': deaths.to_json(orient='index'),
                'size': deaths.shape[0],
            }
        else:
            to_send = {
                'value': recovered.to_json(orient='index'),
                'size': recovered.shape[0],
            }
        return jsonify(to_send)
    to_send = {
        'value': confirmed.to_json(orient='index'),
        'data': data,
        'size': confirmed.shape[0],
        'var': "Confirmed"
    }
    return render_template("index.html", data=to_send)


@app.route("/country", methods=["POST"])
def timeSeries():
    global confirmed_all, recovered_all, deaths_all
    country = request.form['country']
    tmp = confirmed_all[
            confirmed_all['Country/Region'] == country
        ].drop(
            ['Province/State', 'Lat', 'Long', 'Country/Region'],
            axis=1
        ).sum().to_dict()
    cases = []
    for k, v in tmp.items():
        cases.append({'date':pd.to_datetime(k).strftime("%Y-%m-%d"), 'n':v})
    tmp = deaths_all[
            deaths_all['Country/Region'] == country
        ].drop(
            ['Province/State', 'Lat', 'Long', 'Country/Region'],
            axis=1
        ).sum().to_dict()
    deaths = []
    for k, v in tmp.items():
        deaths.append({'date':pd.to_datetime(k).strftime("%Y-%m-%d"), 'n':v})
    tmp = recovered_all[
            recovered_all['Country/Region'] == country
        ].drop(
            ['Province/State', 'Lat', 'Long', 'Country/Region'],
            axis=1
        ).sum().to_dict()
    recovered = []
    for k, v in tmp.items():
        recovered.append({'date':pd.to_datetime(k).strftime("%Y-%m-%d"), 'n':v})
    to_send = {
        'cases': cases,
        'deaths': deaths,
        'recovered': recovered
    }
    return jsonify(to_send)

@app.route("/all_info", methods=["POST"])
def all_info():
    global country_info
    data = country_info.loc[request.form['country']].to_dict()
    maximums = country_info.max(axis=0).to_dict()
    for k in data:
        data[k] = 1.0 * data[k] / maximums[k]
    return jsonify(data)

@app.route("/parallel", methods=["POST"])
def parallel():
    global all_data
    # process
    l = all_data.T.to_dict()
    ans = []
    for k in l:
        d = l[k]
        d['name'] = k
        ans.append(d)
    
    return jsonify(ans)




if __name__ == "__main__":
    confirmed = pd.read_csv('data/world_confirmed.csv')
    deaths = pd.read_csv('data/world_deaths.csv')
    recovered = pd.read_csv('data/world_recovered.csv')
    country_info = pd.read_csv('data/parallel_coor.csv', index_col=0)
    # country_info['']
    confirmed_all = pd.read_csv(
        'data/time_series_covid19_confirmed_global.csv'
    )
    deaths_all = pd.read_csv(
        'data/time_series_covid19_deaths_global.csv'
    )
    recovered_all = pd.read_csv(
        'data/time_series_covid19_recovered_global.csv'
    )
    with open('data/world_countries.json') as f:
        data = json.load(f)
    all_data = pd.read_csv('data/all-info.csv', index_col=0)
    app.run(debug=True)
