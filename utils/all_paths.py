from utils.manipulate import *
from utils.Dijkstras import *
import os

"""
all_paths(<json>):

Finds all shortest paths between all ingredients in given data set.


Input: json object of recipes, with all the unnecessary stuff
Output: JSON object all paths table

Usage: to find the shortest path between two ingredients, simply reference
the json object like you would a matrix, i.e. output['capers']['bulgar']
"""


def all_paths(recipes_json):
    # obtain food list
    dirname = os.path.dirname
    food_list = os.path.join(dirname(dirname(__file__)), 'data/foodList.txt')

    # format food list -- this is what we will parse our recipes against
    ingredients_list = format_ingredients(food_list)

    # get ingredients of each recipe
    recipes_ingredients = get_recipes_ingredients(recipes_json)

    # create an initial adjacency matrix
    dirty_mat = ingredients_to_df(ingredients_list, recipes_ingredients)

    # get proper format of adjacency matrix and obtain the labels
    clean_dict = format_df(dirty_mat)
    clean_df = clean_dict['df']
    columns = clean_dict['cols']

    # find all shortest paths
    paths_table = all_shortest_paths(clean_df, columns)

    return {'paths_table': paths_table, 'clean_df': clean_df}
