import pandas as pd
import numpy as np
from scipy import stats



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

def find_intersection(clean_df, ingredients_array):
    # consider only the rows of the desired ingredients
    df_temp = clean_df.loc[ingredients_array, :]

    # Then consider only the columns that have been paired with all ingredients of interest
    new_cols = df_temp.columns[(dftemp >= 1).all()]

    # Remove rows that are same as column names
    final_df = df_temp.loc[:, new_cols].drop(labels=ingredients_array, axis=1)

    # Rank by examining uniformity of distribution along columns. Penalizing for non-uniformity.
    sums = final_df.sum()
    entropy = stats.entropy(final_df, base=2)
    rankings = np.power(sums, entropy)

    cols = final_df.columns.values
    rankings_list = list(zip(cols, rankings))  # list of tuples (<col_name>, <ranking>)

    return rankings_list
