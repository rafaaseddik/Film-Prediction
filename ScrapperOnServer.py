import time
import urllib.request
import json
import re
import numpy as np
import pandas as pd

class Movie :
    def __init__(self,json_object):
        self.title = json_object['title']
        self.imdb_code = json_object['imdb_code']
        self.year = json_object['year']
        self.imdbRat = json_object['rating']
        self.mpaa = json_object['mpa_rating']
        self.genres = json_object['genres']
        self.runtime = json_object['runtime']
        self.language = json_object['language']
        self.budget = -1
        self.gross = -1
        self.countries = []
        self.prod = ["Unknown"]
        self.starpower = 0
        self.director_starpower = 0
        self.popularity = 0
        self.trilogy = False
        self.trilogy_parts = 0
        self.trilogy_popularity = 0


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
api_key ="f65d6b9a6dd3e4c8493a28d8233b066c"
movies_list = np.load("movielist1554673158.2307246.npy")

def star_power(person_id):
    get_actor_details_url = "https://api.themoviedb.org/3/person/"+str(actor_id)+"?api_key="+api_key+"&language=en-US"
    req4 = urllib.request.Request(url=get_actor_details_url, headers=headers)
    json_file4 = urllib.request.urlopen(req4).read()
    parsed_json4 = json.loads(json_file4)
    return parsed_json4['popularity']
filtered_movies = list(filter(lambda mv : (int(mv.year)<=1999) and mv.language == "English",movies_list))

def export_data():# df = pd.DataFrame([t.__dict__ for t in filtered_movies if t.budget>0])
    df = pd.DataFrame([t.__dict__ for t in filtered_movies])
    print(df)
    writer = pd.ExcelWriter('./pandas_10_test_'+ str(time.time())+'.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Movies')
    df.to_csv("pandas_10_test.csv")

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


progress = 0
errors = 0
start = time.time()
timespent = 0
batch_size = len(filtered_movies)
for movie in filtered_movies:
    try:
        from_imdb_url = "https://api.themoviedb.org/3/find/"+movie.imdb_code+"?api_key="+api_key+"&language=en-US&external_source=imdb_id"
        req = urllib.request.Request(url=from_imdb_url, headers=headers)
        json_file = urllib.request.urlopen(req).read()
        parsed_json = json.loads(json_file)
        try:
            delattr(movie, "director")
        except:
            pass
        if(len(parsed_json['movie_results'])>0):
            tmdb_id = parsed_json['movie_results'][0]['id']
            get_by_id_url = "https://api.themoviedb.org/3/movie/"+str(tmdb_id)+"?api_key="+api_key+"&language=en-US"
            req2 = urllib.request.Request(url=get_by_id_url, headers=headers)
            json_file2 = urllib.request.urlopen(req2).read()
            parsed_json2 = json.loads(json_file2)
            movie.gross = parsed_json2['revenue']
            movie.budget = parsed_json2['budget']
            movie.popularity = parsed_json2['popularity']
            movie.countries = [i['name'] for i in parsed_json2['production_countries']]
            movie.prod = [i['name'] for i in parsed_json2['production_companies']]

            if( parsed_json2['belongs_to_collection'] is not None):
                movie.trilogy = True
                get_trilogy_url = "https://api.themoviedb.org/3/collection/"+str(parsed_json2['belongs_to_collection']['id'])+"?api_key="+api_key+"&language=en-US"
                req5 = urllib.request.Request(url=get_trilogy_url, headers=headers)
                json_file5 = urllib.request.urlopen(req5).read()
                parsed_json5 = json.loads(json_file5)
                movie.trilogy_parts = len(parsed_json5['parts'])
                sum_trilogy_popularity = 0
                for part in parsed_json5['parts']:
                    sum_trilogy_popularity = sum_trilogy_popularity + part['popularity']
                movie.trilogy_popularity = sum_trilogy_popularity / len(parsed_json5['parts'])
            else:
                movie.trilogy = False
                movie.trilogy_parts = 0
                movie.trilogy_popularity = movie.popularity


            get_credits_url = "https://api.themoviedb.org/3/movie/"+str(tmdb_id)+"/credits?api_key="+api_key+"&language=en-US"
            req3 = urllib.request.Request(url=get_credits_url, headers=headers)
            json_file3 = urllib.request.urlopen(req3).read()
            parsed_json3 = json.loads(json_file3)
            actors_ids = [i['id'] for i in parsed_json3['cast'][:3]]
            directors_ids = [i['id'] for i in parsed_json3['crew'] if i['job'] == 'Director']
            sum_actors_popularity = 0
            sum_directors_popularity = 0
            for actor_id in actors_ids:
                sum_actors_popularity = sum_actors_popularity + star_power(actor_id)
            movie.starpower = sum_actors_popularity / max(1,len(actors_ids),1)

            for director_id in directors_ids:
                sum_directors_popularity = sum_directors_popularity + star_power(director_id)
            movie.director_starpower = sum_actors_popularity / max(1,len(directors_ids))
    except Exception as e:
        print("An error has occured during getting infos for "+ movie.title)
        print(e)
    progress += 1
    now = time.time()
    timespent = int(now-start)
    estimated = int((timespent/progress) * (batch_size-progress))
    print("Loading : "+str(100*progress/batch_size)+"%, Elapsed time : "+str(timespent)+" seconds, Estimated time remaining : "+str(estimated)+" seconds  (Errors="+str(errors)+")",end ="\r");
    #for movie in parsed_json['data']['movies'] :
     #   movies_list.append(Movie(movie))

print("Done  !",end="\r")
export_data()