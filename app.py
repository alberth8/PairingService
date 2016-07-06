'''
How to run:
1.  $ sudo mongod
   in new window, $ mongo
2. $ export FLASK_APP=app.py
   $ flask run

NOTE: If run in to importerror. try dropping database. make sure connected too.
'''
import json
import pandas as pd
from flask import Flask, request, jsonify
from pymongo import MongoClient
from utils.all_paths import all_paths
from utils.intersection import find_intersection

app = Flask(__name__)
client = MongoClient('localhost', 27017)  # creates connection

# drop database, then recreate database
client.drop_database('pairings_service')
db = client['pairings_service']

# create paths collection
paths_coll = db.paths_collection

# seed database by opening file for paths_coll and inter_coll
with open('data/paths_collection.json', 'r') as json_file:  # do not write as binary
    paths_table = json.load(json_file)
# insert into mongodb
paths_coll.insert_many(paths_table) 

# obtain saved data frame
with open('data/store_clean.h5', 'rb') as file:
    print('Opening file...')
    clean_df = pd.read_hdf('data/store_clean.h5', 'table')


# test route
@app.route('/', methods=['GET'])
def home():
    return 'xyz'


# need to create another function for repopulating the database
# input: SHOULD be taking info from the database
@app.route('/api/update', methods=['POST'])
def repopulate():

    recipe_data = request.get_json(force=True)['recipe_data']
    output = all_paths(recipe_data)  # which will be clean_df and a json of paths
    new_clean_df = output['clean']
    new_paths_table = output['paths_table']

    # update clean_df and also overwrite its file
    global clean_df  # refers to clean_df in global scope
    clean_df = new_clean_df
    clean_df.to_hdf('data/store_clean.h5', 'table')

    # drop collection
    db.drop_collection("paths_coll")
    # save new paths table
    paths_coll.insert_many(new_paths_table)
    return 'Have a nice day :)'


@app.route('/api/path', methods=['POST'])
def shortest_path():
    # GET: http://127.0.0.1:5000/api/path?from=apples&to=rum
    # source = request.args.get('from')
    # end = request.args.get('to')

    source = request.get_json(force=True)['ingredients'][0]
    end = request.get_json(force=True)['ingredients'][1]
    document = paths_coll.find({source: {'$exists': True}})
    path = document[0][source][end]
    return jsonify(path=path)


@app.route('/api/intersection', methods=['POST'])
def intersection():
    ingredients = request.get_json()['ingredients']
    result = find_intersection(clean_df, ingredients)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)