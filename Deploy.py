from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.request
import json
import numpy as np
import pandas as pd
from joblib import dump, load

app = Flask(__name__)
CORS(app)

model_1 = load('regression/decisionTreeRegressionModel_13_depth.joblib')
model_2 = load('regression/randomForestRegressionModel_13_depth_10_estimators.joblib')

def dict_dummy(observation: dict):
    features_name = ['director_starpower', 'imdbRat', 'runtime', 'starpower',
                     'trilogy_parts', 'trilogy_popularity', 'year',
                     'prod_is_20th Century Fox',
                     'prod_is_American International Pictures (AIP)', 'prod_is_BBC Films',
                     'prod_is_Blumhouse Productions', 'prod_is_Canal+',
                     'prod_is_Columbia Pictures', 'prod_is_DC Entertainment',
                     'prod_is_Dimension Films', 'prod_is_DreamWorks',
                     'prod_is_Dune Entertainment', 'prod_is_Film4 Productions',
                     'prod_is_Fox Searchlight Pictures', 'prod_is_Lionsgate',
                     'prod_is_Metro-Goldwyn-Mayer', 'prod_is_Miramax', 'prod_is_Netflix',
                     'prod_is_New Line Cinema', 'prod_is_Paramount',
                     'prod_is_Relativity Media', 'prod_is_Screen Gems',
                     'prod_is_Silver Pictures', 'prod_is_Sony Pictures',
                     'prod_is_Studio Babelsberg', 'prod_is_StudioCanal',
                     'prod_is_Summit Entertainment', 'prod_is_Touchstone Pictures',
                     'prod_is_TriStar Pictures', 'prod_is_United Artists',
                     'prod_is_Universal Pictures', 'prod_is_Village Roadshow Pictures',
                     'prod_is_Walt Disney Pictures', 'prod_is_Warner Bros. Pictures',
                     'prod_is_Working Title Films', 'prod_is_others', 'genres_is_Action',
                     'genres_is_Adventure', 'genres_is_Animation', 'genres_is_Biography',
                     'genres_is_Comedy', 'genres_is_Crime', 'genres_is_Documentary',
                     'genres_is_Drama', 'genres_is_Family', 'genres_is_Fantasy',
                     'genres_is_Film-Noir', 'genres_is_History', 'genres_is_Horror',
                     'genres_is_Music', 'genres_is_Musical', 'genres_is_Mystery',
                     'genres_is_News', 'genres_is_Reality-TV', 'genres_is_Romance',
                     'genres_is_Sci-Fi', 'genres_is_Sport', 'genres_is_Talk-Show',
                     'genres_is_Thriller', 'genres_is_War', 'genres_is_Western',
                     'countries_is_Australia', 'countries_is_Belgium', 'countries_is_Canada',
                     'countries_is_China', 'countries_is_Czech Republic',
                     'countries_is_Denmark', 'countries_is_Finland', 'countries_is_France',
                     'countries_is_Germany', 'countries_is_Hong Kong', 'countries_is_India',
                     'countries_is_Ireland', 'countries_is_Italy', 'countries_is_Japan',
                     'countries_is_Mexico', 'countries_is_Netherlands',
                     'countries_is_New Zealand', 'countries_is_Poland',
                     'countries_is_Russia', 'countries_is_South Africa',
                     'countries_is_South Korea', 'countries_is_Spain', 'countries_is_Sweden',
                     'countries_is_United Kingdom', 'countries_is_United States of America',
                     'countries_is_others', 'mpaa_is_G', 'mpaa_is_NC-17', 'mpaa_is_PG',
                     'mpaa_is_PG - 13', 'mpaa_is_R']

    result = [0 for i in range(len(features_name))]
    for keys in range(len(features_name)):
        if (features_name[keys] in observation):
            result[keys] = observation[features_name[keys]]

    for country in observation['countries']:
        result[features_name.index("countries_is_" + country)] = 1
    for genre in observation['genres']:
        result[features_name.index("genres_is_" + genre)] = 1
    for p in observation['prod']:
        result[features_name.index("prod_is_" + p)] = 1

    for m in observation['mpaa']:
        result[features_name.index("mpaa_is_" + m)] = 1
    return result

model_1 = load('regression/decisionTreeRegressionModel_13_depth.joblib')
model_2 = load('regression/randomForestRegressionModel_13_depth_10_estimators.joblib')
model_3 = load('regression/XGBRegressor.joblib')

api_key ="f65d6b9a6dd3e4c8493a28d8233b066c"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

def encode_row(row):{

}

class Movie :
    def __init__(self,json_object):
        self.title = json_object.get('title')
        self.imdb_code = json_object.get('imdb_code')
        self.year = json_object.get('year')
        self.imdbRat = json_object.get('imdbRat')
        self.mpaa = json_object.get('mpaa')
        self.genres = json_object.get('genres')
        self.runtime = json_object.get('runtime')
        self.language = json_object.get('language')
        self.countries = json_object.get('countries')
        self.prod = json_object.get('prod')
        self.starpower = json_object.get('starpower')
        self.director_starpower = json_object.get('director_starpower')
        self.trilogy = json_object.get('trilogy')
        self.trilogy_parts = json_object.get('trilogy_parts')
        self.trilogy_popularity = json_object.get('trilogy_popularity')

        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                              sort_keys=True, indent=4)
        #def encode(self):

@app.route("/")
def hello():
    return "Hello World!";


@app.route('/predict', methods=['POST'])
def predict():
    try:
        input = request.get_json(force=True)
        model_number = request.args.get('model')
        movie  = input['movie']

        row = [dict_dummy(movie)]
        prediction = 0
        print(input['movie'])

        if(model_number is 0):
            prediction = model_1.predict(row)
        else :
            prediction = model_2.predict(row)
        output = {
                "row":row,
                "model":model_number,
                "prediction":prediction.tolist()[0]
                }
        return jsonify(output)
    except Exception as e:
        print(e)

@app.route('/autocomplete-person',methods=['GET'])
def autocomplete_person():
    query = request.args.get('query')
    print(query)
    from_query = "https://api.themoviedb.org/3/search/person?api_key=" + api_key + "&language=en-US&query="+query
    req = urllib.request.Request(url=from_query, headers=headers)
    json_file = urllib.request.urlopen(req).read()
    parsed_json = json.loads(json_file)
    return_obj = [{'id':i['id'],'name':i['name'],'popularity':i['popularity']} for i in parsed_json['results']]
    output = {
        "result": return_obj
    }
    return jsonify(output)

@app.route('/autocomplete-prod',methods=['GET'])
def autocomplete_prod():
    output = {
        "result": ['20th Century Fox','American International Pictures (AIP)','BBC Films','Blumhouse Productions','Canal+','Columbia Pictures','DC Entertainment','Dimension Films','DreamWorks','Dune Entertainment','Film4 Productions','Fox Searchlight Pictures','Lionsgate','Metro-Goldwyn-Mayer','Miramax','Netflix','New Line Cinema','Paramount','Relativity Media','Screen Gems','Silver Pictures','Sony Pictures','Studio Babelsberg','StudioCanal','Summit Entertainment','Touchstone Pictures','TriStar Pictures','United Artists','Universal Pictures','Village Roadshow Pictures','Walt Disney Pictures','Warner Bros. Pictures','Working Title Films','others']
    }
    return jsonify(output)

@app.route('/autocomplete-trilogy',methods=['GET'])
def autocomplete_trilogy():
    query = request.args.get('query')
    print(query)
    from_query = "https://api.themoviedb.org/3/search/collection?api_key=" + api_key + "&language=en-US&query="+query
    req = urllib.request.Request(url=from_query, headers=headers)
    json_file = urllib.request.urlopen(req).read()
    parsed_json = json.loads(json_file)
    return_obj = []
    for trilogy in parsed_json['results'] :
        trilogy_dto = {"id":trilogy['id'],"title":trilogy["name"],"trilogy_parts":0}
        get_trilogy_url = "https://api.themoviedb.org/3/collection/" + str(trilogy['id']) + "?api_key=" + api_key + "&language=en-US"
        req5 = urllib.request.Request(url=get_trilogy_url, headers=headers)
        json_file5 = urllib.request.urlopen(req5).read()
        parsed_json5 = json.loads(json_file5)
        trilogy_dto["trilogy_parts"] = len(parsed_json5["parts"])
        sum_trilogy_popularity = 0
        for part in parsed_json5['parts']:
            sum_trilogy_popularity = sum_trilogy_popularity + part['popularity']
        trilogy_dto["trilogy_popularity"] = sum_trilogy_popularity / len(parsed_json5['parts'])
        return_obj.append(trilogy_dto)

    output = {
        "result": return_obj
    }
    return jsonify(output)

@app.route('/genres')
def get_genres():
    return jsonify({
        "genres":['Action','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','Film-Noir','History','Horror','Music','Musical','Mystery','News','Reality-TV','Romance','Sci-Fi','Sport','Talk-Show','Thriller','War','Western']
    })\

@app.route('/countries')
def get_countries():
    return jsonify({
        "countries":['Australia','Belgium','Canada','China','Czech Republic','Denmark','Finland','France','Germany','Hong Kong','India','Ireland','Italy','Japan','Mexico','Netherlands','New Zealand','Poland','Russia','South Africa','South Korea','Spain','Sweden','United Kingdom','United States of America','others'
        ]
    })

@app.route('/stats')
def get_stats():
    full_data = pd.read_csv("data_full.csv").T.to_dict().values()
    max_budget = max(full_data,key=lambda x:x['budget'])
    max_revenue = max(full_data,key=lambda x:x['gross'])
    most_popular = max(full_data,key=lambda x:x['popularity'])
    longest = max(full_data,key=lambda x:x['runtime'])
    return jsonify({
        "max_budget":max_budget,
        "max_revenue":max_revenue,
        "most_popular":most_popular,
        "longuest":longest
    })

if __name__ == "__main__":
    app.run(debug=True,port=5000)