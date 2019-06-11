import numpy as np
from flask import Flask, abort, jsonify, request
from json2html import *
import pickle
import json

# Demographic: popular pickle
popular10 = pickle.load(open("/notebook/flask_app/popular10.pkl", "rb"))
popular_output = popular10[['title', 'vote_count', 'vote_average', 'score']].head(10)

# Content based: darkknight pickle
darkknight = pickle.load(open("/notebook/flask_app/darknight.pkl", "rb"))
darkknight_output = darkknight[['title']].head(10)

# Content based: superman pickle
superman = pickle.load(open("/notebook/flask_app/superman.pkl", "rb"))
superman_output = superman[['title']].head(10)

# Content based: avatar pickle
avatar = pickle.load(open("/notebook/flask_app/avatar.pkl", "rb"))
avatar_output = avatar[['title']].head(10)

# Collaborative based: 
# u1_diehard
u1diehard = pickle.load(open("/notebook/flask_app/u1_diehard.pkl", "rb"))
u1diehard_output = u1diehard[['title', 'vote_count', 'vote_average', 'id', 'est']].head(10)

# u101_avatar
u101avatar = pickle.load(open("/notebook/flask_app/u101_avatar.pkl", "rb"))
u101avatar_output = u101avatar[['title', 'vote_count', 'vote_average', 'id', 'est']].head(10)

# u200_spartacus
u200spartacus = pickle.load(open("/notebook/flask_app/u200_spartacus.pkl", "rb"))
u200spartacus_output = u200spartacus[['title', 'vote_count', 'vote_average', 'id', 'est']].head(10)

app = Flask(__name__)

@app.route('/api/popular', methods=['GET'])
def geographic_filter_api():
    json = popular_output.to_json(orient='records')
    print(json)
    return json

@app.route('/html/popular', methods=['GET'])
def geographic_filter_html():
    table = json2html.convert(popular_output.to_json(orient='records'))
    print(table)
    return table

@app.route('/api/content', methods=['GET'])
def content_filter_api():
    movie = request.args.get('movie')
    print("Requested movie:", movie)
    if movie == 'Dark Knight': 
        out = darkknight_output.to_json(orient='records') 
    elif movie == 'Superman': 
        out = superman_output.to_json(orient='records')
    elif movie == 'Avatar': 
        out = avatar_output.to_json(orient='records')
    else:
        out = 'Not found'
    print(out)
    return out

@app.route('/html/content', methods=['GET'])
def content_filter_html():
    movie = request.args.get('movie')
    print("Requested movie:", movie)
    if movie == 'Dark Knight': 
        out = darkknight_output.to_json(orient='records') 
    elif movie == 'Superman': 
        out = superman_output.to_json(orient='records')
    elif movie == 'Avatar': 
        out = avatar_output.to_json(orient='records')
    else:
        out = 'Not found'
    table = json2html.convert(out)
    return table


@app.route('/api/collaborative', methods=['GET'])
def collaborative_filter_api():
    userid = request.args.get('userid')
    movie = request.args.get('movie')
    print("Requested user:", userid, " and movie:", movie)
    if userid == '1' and movie == 'Die Hard': 
        out = u1diehard_output.to_json(orient='records') 
    elif userid == '101' and movie == 'Avatar': 
        out = u101avatar_output.to_json(orient='records')
    elif userid == '200' and movie == 'Spartacus': 
        out = u200spartacus_output.to_json(orient='records')
    else:
        out = 'Not found'
    return out

@app.route('/html/collaborative', methods=['GET'])
def collaborative_filter_html():
    userid = request.args.get('userid')
    movie = request.args.get('movie')
    print("Requested user:", userid, " and movie:", movie)
    if userid == '1' and movie == 'Die Hard': 
        out = u1diehard_output.to_json(orient='records') 
    elif userid == '101' and movie == 'Avatar': 
        out = u101avatar_output.to_json(orient='records')
    elif userid == '200' and movie == 'Spartacus': 
        out = u200spartacus_output.to_json(orient='records')
    else:
        out = 'Not found'
    table = json2html.convert(out)
    return table

if __name__ == '__main__':
    app.run(host='0.0.0.0')