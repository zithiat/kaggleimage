import numpy as np
from flask import Flask, abort, jsonify, request
import pickle
import pandas as pd
import json

def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan

    
# demographic 
popular_movies = pickle.load(open("/notebook/flask_app/demographic.pkl", "rb"))

# content-based
df2 = pd.read_csv('/notebook/input/tmdb-movie-metadata/tmdb_5000_movies.csv')
df2 = df2.reset_index()
indices_content = pd.Series(df2.index, index=df2['title'])
cosine_content = pickle.load(open("/notebook/flask_app/cosineContent.pkl", "rb"))

# collaborative
indices_collab = pickle.load(open("/notebook/flask_app/indicesCollab.pkl", "rb"))
cosine_collab = pickle.load(open("/notebook/flask_app/cosineCollab.pkl", "rb"))
svd = pickle.load(open("/notebook/flask_app/svdCollab.pkl", "rb"))
smd = pickle.load(open("/notebook/flask_app/smdCollab.pkl", "rb"))

id_map = pd.read_csv('/notebook/input/the-movies-dataset/links_small.csv')[['movieId', 'tmdbId']]
id_map['tmdbId'] = id_map['tmdbId'].apply(convert_int)
id_map.columns = ['movieId', 'id']
id_map = id_map.merge(smd[['title', 'id']], on='id').set_index('title')
indices_map_collab = id_map.set_index('id')

app = Flask(__name__)

@app.route('/popular', methods=['GET'])
def geographic_frilter():
    output = popular_movies[['title', 'vote_count', 'vote_average', 'score']].head(10)
    return output.to_json(orient='records')


@app.route('/content', methods=['GET'])
def content_filter():
    movie = request.args.get('movie')
    output  = get_recommendations(movie)
    return output.to_json(orient='records')


@app.route('/collaborative', methods=['GET'])
def collaborative_filter():
    userid = request.args.get('userid')
    movie = request.args.get('movie')
    print("Requested user:", userid, " and movie:", movie)
    output  = hybrid(userid, movie)
    return output.to_json(orient='records')


def get_recommendations(title):
    # Get the index of the movie that matches the title
    idx = indices_content[title]
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_content[int(idx)]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    return df2['title'].iloc[movie_indices]


def hybrid(userId, title):
    idx = indices_collab[title]
    tmdbId = id_map.loc[title]['id']
    #print(idx)
    movie_id = id_map.loc[title]['movieId']
    
    sim_scores = list(enumerate(cosine_collab[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]
    
    movies = smd.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'id']]
    movies['est'] = movies['id'].apply(lambda x: svd.predict(userId, indices_map_collab.loc[x]['movieId']).est)
    movies = movies.sort_values('est', ascending=False)
    return movies.head(10)

if __name__ == '__main__':
    app.run(host='0.0.0.0')