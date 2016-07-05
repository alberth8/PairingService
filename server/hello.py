# sys.path.insert(0, )
from ..utils.intersection import find_intersection
import json
import pandas as pd
from flask import Flask, request, jsonify
from pymongo import MongoClient


app = Flask(__name__)  # will eventually change to __main__
client = MongoClient('localhost', 27017)  # creates connection
# client.

'''
How to run:
$ export FLASK_APP=server/hello.py
$ flask run

NOTE: If run in to importerror. try dropping database. make sure connected too.
'''



# drop database
client.drop_database('pairings_service')
# recreate database
db = client['pairings_service']  # create database called pairings_service

# create paths and clean collection
paths_coll = db.paths_collection
clean_coll = db.clean_collection

# 1. seed database by opening file for paths_coll and inter_coll
with open('paths_collection.json', 'r') as json_file:  # do not write as binary
    paths_table = json.load(json_file)


paths_coll.insert_many(paths_table)

with open('store_clean.h5', 'rb') as file:
    clean_df = pd.read_hdf('store_clean.h5', 'table')
# print(clean_df.shape)


# 1. add gevet...or whatever
# 2. add cache



# create and insert entire collection
# new_collection = db.new_collection_name
# then just act on new_collection
# -------------
# paths_collection = db.paths
# paths.insert_many([paths_table]) # paths_table is already json object
# intersect.insert_many(clean_df.to_dict()) # load clean_df from store_clean.h5 or will have to convert to json and write to file


'''
Pairing service provides two functionalities:
1. Returning ingredients in intersection:
    - input: request.ingredients
    - output: returned intersection
    NOTE: Should create cache for most commonly searched intersecitons
2. Returning ingredients from Dijkstra's algorithm
    - input: two ingredients
    - output: path of ingredients
'''


@app.route('/', methods=['GET'])
def home():
    return 'xyz'

# need to create another function for repopulating the database
# input: SHOULD be taking info from the database
# @app.route('/api/update', methods=['???'])
# def repopulate():
#     all_paths(updated_records_from_saffrons_mysql) # which will clean_df and `paths` (json) to db


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
    # return 'xyz'

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=6001, debug=True)
