import pandas as pd
import itertools as it
import numpy as np
import json
import functools

pd.set_option('expand_frame_repr', False)

'''
Obtaining the list of ingredients for each recipe. Only interested
in the ingredients, and so have stripped other information such as URL
'''

# NEED TO MODIFY TO EITHER TAKE A PATH OR A JSON
@functools.lru_cache(maxsize=None)
def get_recipes_ingredients(path_or_json):
    if type(path_or_json) is str:
        with open(path_or_json) as recipes:
            data = json.load(recipes)
    else:
        data = path_or_json

    ingredients_per_recipe = []
    for obj in data:
        ingredients_per_recipe.append(obj["ingredients"])

    return ingredients_per_recipe

# print(get_recipes_ingredients('/Users/alberthahn/HACK_REACTOR/PairingService/combinedRecipes.JSON'))

@functools.lru_cache(maxsize=None)
def format_ingredients(path):
    # getting the list of ingredients
    with open(path) as f:
        ing_list = f.readlines()

    ing_list = [ing[:-1].lower() for ing in ing_list]  # remove '\n' and lowercase
    unique_ing_list = list(set(ing_list))  # uniqify
    unique_ing_list = sorted(unique_ing_list)  # sort

    return unique_ing_list


'''
Count number of pairings using a pandas dataframe
'''

# @functools.lru_cache(maxsize=None)
def ingredients_to_df(ingredients, ingredients_per_recipe):
    df = pd.DataFrame(0, index=ingredients, columns=ingredients)
    for ingredient_list in ingredients_per_recipe:
        for pair in list(it.permutations(ingredient_list, 2)):
            try:
                # count += 1
                r = pair[0]
                c = pair[1]
                curr_value = df.loc[r, c]
                new_value = curr_value + 1
                df.ix[r, c] = new_value
            except KeyError as key_err:
                print('Could not find key in foodList:', key_err)

    # diagonal should be set to 0 because no such case that
    # apples will be paired with apples
    df.values[[np.arange(len(ingredients))]*2] = 0

    return df

'''
format_df():
 Removes rows and columns that have all zeros as this indicates that there are no
 connections with other ingredients. Also converts values to probabilities.

 Input:
    - dataframe

 Return:
    - object: new column names and formated dataframe
'''

# @functools.lru_cache(maxsize=None)
def format_df(df):
    # Now need to remove row and columns that have all 0s
    df = df.loc[:, (df != 0).any(axis=0)]
    df = df.loc[(df != 0).any(axis=1), :]
    # print(df.shape)  # -> (371, 371)

    # convert values to probability
    total = df.sum().sum()  # total sum of df
    df = df.divide(float(-total)).add(1)
    df = df.replace(1.0, 0.0)  # b/c 0 value cells had 1.0 added to it, need to undo

    # get new column names, will need later
    new_cols = list(df.columns.values)

    return {'cols': new_cols, 'df': df}

def sanity_check(df):
    # check for symmetry: A^T = A
    if not np.diag(df).sum():
        raise Exception('Diagonal should be all zeros')
    if not len((df.transpose() == df).all()) == (df.transpose() == df).all().sum():
        raise Exception('Matrix is not symmetric. An error occurred during data frame manipulation.')
    if not list(df.columns.values) == list(df.index.values):
        raise Exception('Column labels do not match row labels.')