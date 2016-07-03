import pandas as pd

'''
NEED TO CREATE A CACHE!!! have it hold on to the top 200 most common combinations

otherwise will need to compute

assuming I can some how get the CLEAN adjacency matrix from database...

0. input: array of ingredients
1. get df from database (odo?)
2. grab all rows of all ingredients user gave me
3. first things first, remove all the columns that match those ingredients (see note below)
3. then we only consider what's in common, that means if any row intersecting
   any one of our columns has a 0, then discard that column
4. then we have to consider the distribution of the numbers over the columns.
    the closer it is to a uniform distribution, the higher ranked it should be.
    as a naiive approach, we just sum down the columns and rank. if there's no time
    left, just do this.

    NOTE: WE ALSO DON'T WANT TO CONSIDER COLUMNS THAT ARE IN THE INGREDIENT SET.
5. return ranked labels


WOULD HAVE LIKED TO USE CHI SQUARED TEST, BUT LACKED DATA
'''

#
# TODO: WHERE TO CACHE?
#

def find_intersection(ingredients_array):
    # TODO: 1. assuming can grab clean_df from database
    df_temp = clean_df.loc[ingredients_array, :]

    # 2. consider only the rows of interest
    sub_df = df_temp.columns[(dftemp >= 1).all()]

    # TODO: 3. since nxn, remove rows that are same as column names. Is it possible to chain to above?

    # TODO: 4. rank by examining uniformity of distribution along columns
    # NAIVE: sum the total times they are paired and sort to obtain rank
    # ranked = dftemp.loc[:, sub_df].sum(axis=0).sort_values(ascending=False, kind='mergesort')  # type Series

    return ranked.index.values  # a series, so now return an array of the row labels

