from utils.manipulate import *
from utils.Dijkstras import *

'''
all_paths(<json>):

finds all shortest paths between all ingredients in given data set.


input: json object of recipes, with all the unnecessary stuff
output: JSON object all paths table

usage: to find the shortest path between two ingredients, simply reference
the json object like you would a matrix, i.e. output['capers']['bulgar']

Note:

Since this is being called weekly by a worker, we have to be able to have
ingredients_list persist somewhere. But worst case is recalculating it
every time.
'''


def all_paths(recipes_json):
    # assuming recipes_ingredients persists in memory

    # get ingredients of each recipe
    recipes_ingredients = get_recipes_ingredients(recipes_json)

    # create an initial adjacency matrix
    dirty_mat = ingredients_to_df(ingredients_list, recipes_ingredients)

    # get proper format of adjacency matrix and obtain the labels
    clean_dict = format_df(dirty_mat)
    clean_df = clean_dict['df']
    columns = clean_dict['cols']

    #
    # TODO: save clean_df and columns to database
    #

    # find all shortest paths
    pairings_table = all_shortest_paths(clean_df, columns)

    return pairings_table
