import numpy as np
from scipy import stats

'''
find_intersection():
 Finds commonly paired ingredients with the ingredients the user has given.

 We rank by two factors: distribution and cardinality. First we consider
 only ingredients that have been paired with all ingredients selected by the
 user (rows). Next, we examine the distribution of each of those intersections (columns).
 How this is measured is by entropy, using log base 2 (shannons). Maximum entropy
 is obtained in a uniform distribution, and so the more well distributed the
 ingredients are, the higher it's entropy is. Lower bound is at 0.

 However, total count is also important, as it represents frequency. So we must
 factor in both variables. In order to address sets that heavily bias
 towards one or a select few of ingredients, each count raised to the power of it's
 entropy. This essentially rewards ingredients that are more well distributed.

Input:
 - clean_df: cleaned adjacency matrix
 - user_ingredients: list of ingredients provided by user

Output:
 - rankings_list: a list of tuples in ranked order
'''


def find_intersection(clean_df, user_ingredients):
    # consider only the rows of the desired user_ingredients
    df_temp = clean_df.loc[user_ingredients, :]

    # drop columns that match `user_ingredients`. Examining shape of df_temp before and after,
    # column size decreases by 2
    df_temp = df_temp.drop(labels=user_ingredients, axis=1)

    # Then consider only the columns that have been paired with all ingredients of interest
    new_cols = df_temp.columns[(df_temp > float(0)).all()]

    # Remove rows that are same as column names
    final_df = df_temp.loc[:, new_cols]

    # Rank by examining uniformity of distribution along columns. Penalizing for non-uniformity.
    sums = final_df.sum()
    entropy = stats.entropy(final_df, base=2)
    rankings = np.power(sums, entropy)
    rankings_sorted = rankings.sort_values()

    # format into list of tuples (<col_name>, <ranking>)
    cols = rankings_sorted.index.values
    rankings_list = list(zip(cols, rankings))

    return rankings_list
