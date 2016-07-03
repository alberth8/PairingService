from flask import Flask
# from flask import request
# from utils.intersection import *  # for getting intersection of ingredients
app = Flask(__name__) # will eventually change to __main__


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


@app.route('/api/pairings', methods=['GET'])
def pairings():
    # call intersection function
    return 'Returning recommended ingredient pairings...'


@app.route('/api/intersection', methods=['GET'])
def shortest_path():
    # query database, then return results
    return 'Hello, World'

if __name__ == '__main__':
    app.run()