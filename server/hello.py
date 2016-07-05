import json
import pandas as pd
from flask import Flask
from pymongo import MongoClient
from flask import request, jsonify
from utils.intersection import *  # for getting intersection of ingredients

app = Flask(__name__)  # will eventually change to __main__

'''
How to run:
$ export FLASK_APP=hello.py
$ flask run
'''

client = MongoClient('localhost', 27017)  # creates connection

# drop database
client.drop_database('pairings_service')
# recreate database
db = client['pairings_service']  # create database called pairings_service

# create paths and clean collection
paths_coll = db.paths_collection
clean_coll = db.clean_collection

# TODO:
# 1. seed database by opening file for paths_coll and inter_coll
with open('paths_collection.json', 'r') as json_file:  # do not write as binary
    paths_table = json.load(json_file)
# print(type(paths_table))
paths_coll.insert_many(paths_table)

# ----------------------------------------------------
# Not sure if will need to store clean_df in database
#
with open('clean_collection.json', 'r') as clean:  # do not write as binary
    clean_df = json.load(clean)
clean_coll.insert_many(clean_df)
#
#
# ----------------------------------------------------

with open('store_clean.h5', 'rb') as file:
    clean_df = pd.read_hdf('store_clean.h5', 'table')
print(clean_df.shape)




# 2. test in mongo if the queries work
# test = paths_coll.find({'applez': {'$exists': True}})
# print(test[0])
# print(test[0]['apple']['rum'])

# 3. test if routes work, use dummy data (global variables in server)
# 4. add gevet...or whatever






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
    return jsonify(a=2, b=3)

# need to create another function for repopulating the database
# input: SHOULD be taking info from the database
# @app.route('/api/update', methods=['???'])
# def repopulate():
#     all_paths(updated_records_from_saffrons_mysql) # which will clean_df and `paths` (json) to db


@app.route('/api/path', methods=['GET'])
def shortest_path():
    ingredient_a = request.ingredients[0]
    ingredient_b = request.ingredients[1]
    doc = paths_coll.find({ingredient_a: {'$exists': True}})
    path = doc[0][ingredient_a][ingredient_b]
    return jsonify(path)


@app.route('/api/intersection', methods=['GET'])
def intersection():
    ingredients = request.ingredients  # type list
    set = find_intersection(clean_df, ingredients)
    return jsonify(set)

if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=6001, debug=True)
