from flask import Flask
from flask import render_template, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from sklearn.metrics import pairwise_distances
import matplotlib.pyplot as plt



app = Flask(__name__)

data_covid = pd.read_csv('data/country-latest.csv')
data_parallel = pd.read_csv('data/parallel_coor.csv')

data_covid.drop(columns=['Province/State', 'Lat', 'Long'],inplace=True)
data_covid.rename(columns={'Country/Region':'country'}, inplace=True)
data_covid.recovered.fillna(0,inplace=True)
data_covid = data_covid.groupby('country').sum().reset_index()

data_parallel.rename(columns={'Unnamed: 0':'country'}, inplace=True)
for col in data_parallel.columns[1:]:
    data_parallel[col].fillna(data_parallel[col].median(),inplace=True)
data_parallel.country.replace({'Bahamas, The':'Bahamas', 'Brunei Darussalam':'Brunei','Myanmar':'Burma','Congo, Dem. Rep.':'Congo (Kinshasa)','Congo, Rep.':'Congo (Brazzaville)','Czech Republic':'Czechia','Egypt, Arab Rep.':'Egypt','Gambia, The':'Gambia','Iran, Islamic Rep.':'Iran','Korea, Rep.':'Korea, South','Kyrgyz Republic':'Kyrgyzstan','Lao PDR':'Laos','Russian Federation':'Russia','St. Kitts and Nevis':'Saint Kitts and Nevis','St. Lucia':'Saint Lucia','St. Vincent and the Grenadines':'Saint Vincent and the Grenadines','Slovak Republic':'Slovakia','Syrian Arab Republic':'Syria','United States':'US','Venezuela, RB':'Venezuela','Yemen, Rep.':'Yemen'},inplace=True)

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/parallel_coordinate_graph')
def parallel_coordinate_graph():
    data_parallel_visualization = pd.merge(data_covid,data_parallel,on='country')
    return json.dumps(data_parallel_visualization.to_dict(orient='records'))#json.loads(data_parallel_visualization.to_json(orient='records'))#pd.json.dumps(data_parallel_visualization)

if __name__ == "__main__":
    app.run(debug=True)
